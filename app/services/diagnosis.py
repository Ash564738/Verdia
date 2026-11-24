from __future__ import annotations

import base64
import hashlib
import io
import json
from collections import Counter
from pathlib import Path
from typing import Any
import logging
import time

from PIL import Image

logger = logging.getLogger("smart-plant-care.diagnosis")


class DiagnosisService:
    """Inference boundary with an optional TorchScript model."""

    def __init__(self) -> None:
        self.model_status = "fallback"
        self._model = None
        self._transform = None
        self._cam_layer_name: str | None = None
        self._input_size = 224
        self._confidence_threshold = 0.60
        self._predictions: list[dict[str, Any]] = []
        self._labels = ["healthy", "apple_scab", "tomato_early_blight", "potato_late_blight"]

    def load(self) -> None:
        checkpoint = Path(__file__).parents[2] / "models" / "plant_health.pt"
        state_checkpoint = checkpoint.with_suffix(".pth")
        labels_file = checkpoint.with_suffix(".labels.txt")
        metadata_file = checkpoint.with_suffix(".metadata.json")
        metadata: dict[str, Any] = {}
        logger.info("model_load_started torchscript_exists=%s state_dict_exists=%s labels_exists=%s metadata_exists=%s", checkpoint.exists(), state_checkpoint.exists(), labels_file.exists(), metadata_file.exists())
        if labels_file.exists():
            self._labels = [line.strip() for line in labels_file.read_text().splitlines() if line.strip()]
        if metadata_file.exists():
            import json
            metadata = json.loads(metadata_file.read_text(encoding="utf-8"))
        threshold_file = checkpoint.with_suffix(".threshold.json")
        if threshold_file.exists():
            threshold_config = json.loads(threshold_file.read_text(encoding="utf-8"))
            candidate_threshold = float(threshold_config.get("confidence_threshold", self._confidence_threshold))
            if 0.0 <= candidate_threshold <= 1.0:
                self._confidence_threshold = candidate_threshold
            else:
                logger.warning("model_threshold_invalid value=%s; using default=0.6", candidate_threshold)
        if not checkpoint.exists() and not state_checkpoint.exists():
            logger.warning("diagnosis_checkpoint_missing path=%s", checkpoint)
            return
        try:
            import torch
            from torch import nn
            from torchvision import transforms

            if state_checkpoint.exists():
                from torchvision import models

                architecture = metadata.get("architecture", "efficientnet_b0")
                constructors = {
                    "efficientnet_b0": models.efficientnet_b0,
                    "mobilenet_v3_small": models.mobilenet_v3_small,
                    "resnet18": models.resnet18,
                }
                if architecture not in constructors:
                    raise ValueError(f"Unsupported model architecture: {architecture}")
                self._model = constructors[architecture](weights=None)
                if architecture == "efficientnet_b0":
                    self._model.classifier[1] = nn.Linear(self._model.classifier[1].in_features, len(self._labels))
                elif architecture == "mobilenet_v3_small":
                    self._model.classifier[3] = nn.Linear(self._model.classifier[3].in_features, len(self._labels))
                else:
                    self._model.fc = nn.Linear(self._model.fc.in_features, len(self._labels))
                payload = torch.load(state_checkpoint, map_location="cpu", weights_only=True)
                self._model.load_state_dict(payload["state_dict"], strict=True)
                self._cam_layer_name = metadata.get("gradcam_layer")
                self.model_status = "pytorch"
            else:
                self._model = torch.jit.load(str(checkpoint), map_location="cpu").eval()
                self.model_status = "torchscript"
            self._model.eval()
            self._input_size = int(metadata.get("image_size", 224))
            self._transform = transforms.Compose(
                [
                    transforms.Resize((self._input_size, self._input_size)),
                    transforms.ToTensor(),
                    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
                ]
            )
            self._model_version = str(metadata.get("version", "1.0.0"))
            actual_path = state_checkpoint if state_checkpoint.exists() else checkpoint
            fingerprint = hashlib.sha256(actual_path.read_bytes()).hexdigest()
            logger.info("model_load_succeeded source=%s architecture=%s version=%s class_count=%s image_size=%s threshold=%.6f checkpoint_bytes=%s checkpoint_sha256=%s", "pytorch_state_dict" if state_checkpoint.exists() else "torchscript", metadata.get("architecture", "unknown"), self._model_version, len(self._labels), self._input_size, self._confidence_threshold, actual_path.stat().st_size, fingerprint)
        except Exception as exc:
            self.model_status = f"checkpoint_unavailable:{type(exc).__name__}"
            self._model = None
            self._transform = None
            logger.exception("model_load_failed exception_type=%s", type(exc).__name__)

    def info(self) -> dict[str, Any]:
        """Non-secret model and runtime diagnostics for the model info endpoint."""
        root = Path(__file__).parents[2]
        checkpoint = root / "models" / "plant_health.pt"
        state_checkpoint = checkpoint.with_suffix(".pth")
        metadata_path = checkpoint.with_suffix(".metadata.json")
        training_path = checkpoint.with_suffix(".training.json")
        evaluation_path = checkpoint.with_suffix(".evaluation.json")
        metadata = json.loads(metadata_path.read_text(encoding="utf-8")) if metadata_path.exists() else {}
        training = json.loads(training_path.read_text(encoding="utf-8")) if training_path.exists() else {}
        evaluation = json.loads(evaluation_path.read_text(encoding="utf-8")) if evaluation_path.exists() else {}
        active_path = state_checkpoint if self._model is not None and state_checkpoint.exists() else checkpoint
        import torch

        return {
            "status": self.model_status,
            "loaded": self._model is not None and self._transform is not None,
            "architecture": metadata.get("architecture"),
            "version": getattr(self, "_model_version", "1.0.0"),
            "class_count": len(self._labels),
            "classes": self._labels,
            "image_size": self._input_size,
            "confidence_threshold": self._confidence_threshold,
            "checkpoint": active_path.name if active_path.exists() else None,
            "checkpoint_bytes": active_path.stat().st_size if active_path.exists() else None,
            "checkpoint_sha256": hashlib.sha256(active_path.read_bytes()).hexdigest() if active_path.exists() else None,
            "torch_version": torch.__version__,
            "cuda_available": torch.cuda.is_available(),
            "training_complete": training.get("complete"),
            "completed_epochs": training.get("completed_epochs"),
            "requested_epochs": training.get("requested_epochs"),
            "plantvillage_test_accuracy": evaluation.get("accuracy"),
            "plantvillage_test_macro_f1": evaluation.get("macro_f1"),
        }

    @staticmethod
    def _normalize_crop(value: str) -> str:
        crop = value.strip().lower().replace("_", " ")
        return {
            "pepper, bell": "bell pepper", "bell pepper": "bell pepper",
            "corn (maize)": "corn", "maize": "corn",
            "cherry (including sour)": "cherry",
        }.get(crop, crop)

    def predict(self, image: Image.Image, request_id: str = "-", expected_species: str | None = None) -> dict[str, Any]:
        started = time.perf_counter()
        original_mode = image.mode
        logger.info("diagnosis_inference_started request_id=%s width=%s height=%s source_mode=%s model_status=%s threshold=%.6f", request_id, image.width, image.height, original_mode, self.model_status, self._confidence_threshold)
        if image.width < 32 or image.height < 32:
            logger.warning("diagnosis_inference_rejected request_id=%s reason=dimensions width=%s height=%s", request_id, image.width, image.height)
            raise ValueError("Image dimensions must be at least 32x32 pixels")

        if self._model is not None and self._transform is not None:
            import torch

            try:
                rgb_image = image.convert("RGB")
                tensor = self._transform(rgb_image).unsqueeze(0)
                with torch.inference_mode():
                    logits = self._model(tensor)
                    probabilities = torch.softmax(logits, dim=1)[0]
                if not torch.isfinite(probabilities).all():
                    raise RuntimeError("Model output contains NaN or infinite probabilities")
            except Exception:
                logger.exception("diagnosis_inference_failed request_id=%s stage=forward", request_id)
                raise
            global_index = int(probabilities.argmax())
            global_label = self._labels[global_index]
            global_plant, _ = self._split_label(global_label)
            expected_crop = self._normalize_crop(expected_species) if expected_species else None
            crop_mismatch = False
            if expected_crop:
                crop_indices = [i for i, candidate in enumerate(self._labels)
                                if self._normalize_crop(self._split_label(candidate)[0]) == expected_crop]
                if not crop_indices:
                    raise ValueError(f"No model classes are available for selected crop: {expected_species}")
                crop_mismatch = self._normalize_crop(global_plant) != expected_crop
                ranked = sorted(crop_indices, key=lambda i: float(probabilities[i]), reverse=True)[:3]
                top_indices = torch.tensor(ranked, dtype=torch.long)
                top_values = probabilities[top_indices]
                index = ranked[0]
            else:
                top_values, top_indices = torch.topk(probabilities, k=min(3, len(probabilities)))
                index = int(top_indices[0])
            label = self._labels[index] if index < len(self._labels) else f"class_{index}"
            confidence = float(probabilities[index])
            recommendation = "Follow the crop-specific treatment guidance and consult an agronomist for severe symptoms."
        else:
            label = "healthy"
            confidence = 0.5
            recommendation = "No trained checkpoint is loaded. Run scripts/train.py before using this result."
            top_values, top_indices = [], []
        record = {"label": label, "confidence": confidence}
        self._predictions.append(record)
        plant_name, disease_name = self._split_label(label)
        disease_key = disease_name.lower()
        disease_info = {
            "bacterial": {
                "name_vi": "Bệnh đốm vi khuẩn",
                "symptoms": "Vết ướt nâu/xám, có thể lan nhanh và làm lá héo.",
                "cause": "Vi khuẩn phát triển mạnh trong điều kiện ấm, ẩm và lá bị thương.",
                "treatment": "Cách ly lá/cây nghi bệnh, loại bỏ lá nặng, vệ sinh dụng cụ và tham khảo cán bộ chuyên môn về biện pháp khuyến cáo địa phương.",
                "prevention": "Tưới vào gốc, tránh tưới làm lá ướt, luân canh và chọn giống phù hợp.",
            },
            "blight": {
                "name_vi": "Bệnh cháy lá/đốm lá",
                "symptoms": "Vết nâu/sẫm màu lan trên lá, lá già có thể bị tổn thương trước.",
                "cause": "Thường liên quan nấm hoặc vi khuẩn và điều kiện lá ẩm kéo dài.",
                "treatment": "Loại bỏ lá bị bệnh nặng bằng dụng cụ sạch, giữ tán lá thông thoáng và theo dõi diễn tiến.",
                "prevention": "Giữ lá khô, tránh tưới lên lá và kiểm tra cây định kỳ.",
            },
            "mildew": {
                "name_vi": "Bệnh phấn/trắng phấn",
                "symptoms": "Vùng trắng hoặc bạc trên lá, sau đó lá có thể vàng và rụng.",
                "cause": "Nấm phát triển trong môi trường ẩm và thông thoáng kém.",
                "treatment": "Loại bỏ lá nặng bệnh, tăng thông thoáng và theo dõi; tham khảo chuyên gia trước khi dùng hóa chất.",
                "prevention": "Không tưới lên lá, tách gốc cây đủ khoảng cách và vệ sinh lá rụng.",
            },
            "rust": {
                "name_vi": "Bệnh gỉ sắt",
                "symptoms": "Đốm màu cam/vàng nâu trên mặt lá.",
                "cause": "Nấm gỉ phát triển khi lá ẩm kéo dài.",
                "treatment": "Loại bỏ lá bị nặng, tránh để lá ướt lâu và theo dõi lại sau vài ngày.",
                "prevention": "Tưới gốc, tăng thông thoáng và luân canh cây trồng.",
            },
            "mosaic": {
                "name_vi": "Bệnh khảm/đốm virus",
                "symptoms": "Mảng xanh-vàng xen kẽ, lá biến dạng hoặc còi cọc.",
                "cause": "Thường do virus và có thể lây qua côn trùng hoặc dụng cụ.",
                "treatment": "Cách ly cây nghi nhiễm, loại bỏ tàn dư và kiểm soát côn trùng mang bệnh.",
                "prevention": "Vệ sinh dụng cụ, dùng cây giống khỏe và kiểm soát tuyến trùng/rệp.",
            },
            "healthy": {
                "name_vi": "Lá khỏe mạnh",
                "symptoms": "Không phát hiện dấu hiệu tổn thương rõ ràng trên vùng lá đã phân tích.",
                "cause": "Không phát hiện lớp bệnh trong dự đoán của mô hình.",
                "treatment": "Tiếp tục chăm sóc bình thường và chụp lại nếu lá xuất hiện biểu hiện mới.",
                "prevention": "Duy trì tưới đúng, dinh dưỡng cân bằng, thông thoáng và vệ sinh lá rụng.",
            },
        }
        matched = next((info for key, info in disease_info.items() if key in disease_key), None)
        if matched is None:
            matched = {
                "name_vi": disease_name or "Chưa xác định",
                "symptoms": "Mô hình phát hiện một lớp bệnh trong tập dữ liệu huấn luyện.",
                "cause": "Nguyên nhân cụ thể cần xác nhận bởi người có chuyên môn.",
                "treatment": "Không tự dùng hóa chất; cách ly lá nghi bệnh và tham khảo cán bộ chuyên môn.",
                "prevention": "Theo dõi lá mới, giữ ẩm độ phù hợp và vệ sinh dụng cụ.",
            }
        supported_crops = {
            "Apple", "Bell Pepper", "Blueberry", "Cherry", "Corn", "Orange",
            "Grape", "Peach", "Potato", "Raspberry", "Soybean",
            "Squash", "Strawberry", "Tomato",
        }
        normalized_plant = plant_name.strip().lower()
        normalized_plant = {
            "pepper, bell": "bell pepper",
            "bell pepper": "bell pepper",
            "corn (maize)": "corn",
        }.get(normalized_plant, normalized_plant)
        if expected_species and self._normalize_crop(expected_species) not in {crop.lower() for crop in supported_crops}:
            status = "unsupported_crop"
        elif normalized_plant not in {crop.lower() for crop in supported_crops}:
            status = "unsupported_crop"
        elif expected_species and crop_mismatch:
            status = "uncertain"
        elif confidence < self._confidence_threshold:
            status = "uncertain"
        elif label == "healthy" or label.endswith("_healthy") or "healthy" in disease_name.lower():
            status = "healthy"
        else:
            status = "diagnosed"
        disease_code = "healthy" if status == "healthy" else label.lower().replace("___", "_").replace(" ", "_")
        if self._model is not None:
            top_predictions = [
                {
                    "class": self._labels[int(class_index)] if int(class_index) < len(self._labels) else f"class_{int(class_index)}",
                    "confidence": round(float(value), 4),
                }
                for value, class_index in zip(top_values, top_indices)
            ]
        else:
            top_predictions = [{"class": label, "confidence": round(confidence, 4)}]
        explainability = self.explain(image, index) if self._model is not None and not crop_mismatch else {
            "available": False,
            "message": "A model disagreement makes a crop-specific heatmap misleading." if self._model is not None else "A trained checkpoint is required for explainability.",
        }
        prediction = {
            "status": status,
            "confidence": round(confidence, 4),
            "top_predictions": top_predictions,
        } if status != "unsupported_crop" else None
        uncertain = status in {"uncertain", "unknown_disease"}
        display_plant = expected_species if expected_species and status != "unsupported_crop" else plant_name
        response = {
            "diagnosis": "uncertain" if uncertain else label,
            "confidence": confidence,
            "model": {"name": self.model_status, "version": getattr(self, "_model_version", "1.0.0")},
            "recommendation": ("Retake a sharp, well-lit leaf photo. The model disagrees with the selected crop, so no disease conclusion is provided." if crop_mismatch else "Retake a sharp, well-lit leaf photo. Confidence is too low for a disease conclusion.") if uncertain else matched["treatment"],
            "plant": {"name": display_plant, "name_vi": display_plant},
            "disease": {
                "code": "uncertain" if uncertain else disease_code,
                "name": "Uncertain" if uncertain else disease_name,
                "name_vi": "Chưa xác định" if uncertain else matched["name_vi"],
            },
            "symptoms": "Cannot confirm disease symptoms from this image." if uncertain else matched["symptoms"],
            "cause": "Unknown; retake a clearer image or consult a plant specialist." if uncertain else matched["cause"],
            "prevention": "Monitor the plant and retake a clear leaf photo; do not apply disease-specific treatment yet." if uncertain else matched["prevention"],
            "expected_species": expected_species,
            "model_top_species": global_plant if self._model is not None else None,
            "species_mismatch": crop_mismatch if self._model is not None else False,
            "health_assessment": {
                "status": "healthy" if status == "healthy" else "disease_detected" if status == "diagnosed" else "needs_review",
                "risk": "none" if status == "healthy" else "unassessed",
                "confidence": round(confidence, 4),
                "scope": "Chỉ đánh giá vùng lá trên ảnh, không xác định sức khỏe rễ, dinh dưỡng đất hoặc cả cây.",
            },
            "status": status,
            "prediction": prediction,
            "severity": "none" if status == "healthy" else "unassessed",
            "explainability": explainability,
        }
        if status == "unsupported_crop":
            response["message"] = "Loại cây này chưa nằm trong phạm vi hỗ trợ của mô hình."
        elif status == "uncertain":
            response["message"] = (
                f"Bạn chọn {expected_species}, nhưng mô hình đang nghiêng về {global_plant}. "
                "Kết quả dưới đây chỉ là các lớp trong loài đã chọn; hãy kiểm tra lại loài và chụp ảnh lá rõ hơn."
                if crop_mismatch else "Mô hình chưa đủ tin cậy để đưa ra kết luận."
            )
        logger.info("diagnosis_predict_completed request_id=%s expected_species=%s model_top_species=%s species_mismatch=%s status=%s label=%s plant=%s disease=%s confidence=%.6f threshold=%.6f top_k=%s duration_ms=%.2f", request_id, expected_species or "none", global_plant if self._model is not None else "none", crop_mismatch if self._model is not None else False, status, label, display_plant, disease_name, confidence, self._confidence_threshold, top_predictions, (time.perf_counter() - started) * 1000)
        return response

    def require_model(self) -> None:
        if self._model is None or self._transform is None:
            raise RuntimeError("A trained model checkpoint is not available. Deploy models/plant_health.pt before enabling diagnosis.")

    def explain(self, image: Image.Image, target: int) -> dict[str, Any]:
        """Create Grad-CAM when a hookable PyTorch checkpoint is available."""
        import torch

        if self._cam_layer_name:
            layers = dict(self._model.named_modules())
            layer = layers.get(self._cam_layer_name)
            if layer is not None:
                activations: list[torch.Tensor] = []
                gradients: list[torch.Tensor] = []

                def capture(_module: Any, _inputs: Any, output: torch.Tensor) -> None:
                    activations.append(output)
                    output.register_hook(lambda gradient: gradients.append(gradient))

                handle = layer.register_forward_hook(capture)
                try:
                    tensor = self._transform(image).unsqueeze(0)
                    self._model.zero_grad(set_to_none=True)
                    logits = self._model(tensor)
                    logits[0, target].backward()
                finally:
                    handle.remove()
                if activations and gradients:
                    activation, gradient = activations[-1].detach(), gradients[-1].detach()
                    weights = gradient.mean(dim=(2, 3), keepdim=True)
                    cam = torch.relu((weights * activation).sum(dim=1, keepdim=True))
                    cam = torch.nn.functional.interpolate(cam, size=(self._input_size, self._input_size), mode="bilinear", align_corners=False)[0, 0]
                    cam -= cam.min()
                    maximum = float(cam.max())
                    if maximum:
                        cam /= maximum
                    heat = cam.cpu().numpy()
                    import numpy as np

                    red = np.clip(1.5 * heat - 0.25, 0, 1)
                    green = np.clip(1.25 - np.abs(2 * heat - 1.0) * 1.25, 0, 1)
                    blue = np.clip(1.0 - 1.5 * heat, 0, 1)
                    colors = np.stack([red, green, blue], axis=-1)
                    colors = (colors * 255).astype(np.uint8)
                    colors_image = Image.fromarray(colors).resize(image.size)
                    overlay = Image.blend(image.convert("RGB"), colors_image, 0.42)
                    buffer = io.BytesIO()
                    overlay.save(buffer, format="PNG")
                    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
                    return {"available": True, "method": "grad-cam", "heatmap": f"data:image/png;base64,{encoded}"}

        tensor = self._transform(image).unsqueeze(0).requires_grad_(True)
        self._model.zero_grad()
        logits = self._model(tensor)
        logits[0, target].backward()
        gradient = tensor.grad.detach().abs().amax(dim=1)[0]
        gradient -= gradient.min()
        maximum = float(gradient.max())
        if maximum:
            gradient /= maximum
        heat = (gradient.mul(255).byte().cpu().numpy())
        heat_image = Image.fromarray(heat).resize(image.size)
        overlay = Image.new("RGB", image.size, (255, 0, 0))
        overlay.putalpha(heat_image)
        blended = Image.blend(image.convert("RGBA"), overlay, 0.35)
        buffer = io.BytesIO()
        blended.save(buffer, format="PNG")
        encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
        return {"available": True, "method": "input-gradient", "heatmap": f"data:image/png;base64,{encoded}"}

    @staticmethod
    def _split_label(label: str) -> tuple[str, str]:
        normalized = label.strip().replace("_", " ")
        prefixes = [
            ("Tomato", "Tomato"),
            ("Bell pepper", "Bell pepper"),
            ("Potato", "Potato"),
            ("Corn", "Corn"),
            ("Grape", "Grape"),
            ("Apple", "Apple"),
            ("Peach", "Peach"),
            ("Strawberry", "Strawberry"),
            ("Raspberry", "Raspberry"),
            ("Soybean", "Soybean"),
            ("Squash", "Squash"),
            ("Blueberry", "Blueberry"),
            ("Cherry", "Cherry"),
        ]
        for prefix, plant_name in prefixes:
            if normalized.lower().startswith(prefix.lower()):
                disease = normalized[len(prefix):].strip(" _")
                if not disease:
                    disease = "Leaf condition"
                return plant_name, disease or "Leaf condition"
        if "___" in label:
            plant, disease = label.split("___", 1)
            return plant.replace("_", " "), disease.replace("_", " ")
        if "_" in label:
            plant, disease = label.split("_", 1)
            return plant.title(), disease.replace("_", " ").title()
        return "Unknown", label.replace("_", " ").title()

    def analytics(self) -> dict[str, Any]:
        total = len(self._predictions)
        distribution = Counter(item["label"] for item in self._predictions)
        average = (
            sum(item["confidence"] for item in self._predictions) / total
            if total
            else 0.0
        )
        return {
            "total_predictions": total,
            "average_confidence": round(average, 4),
            "class_distribution": dict(distribution),
        }
