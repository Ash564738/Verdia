from __future__ import annotations

import argparse
import csv
import json
import logging
import random
import time
from collections import defaultdict
from pathlib import Path


def configure_logging(log_path: Path, level: str) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler(log_path, encoding="utf-8")],
        force=True,
    )


def make_model(torch, models, nn, architecture: str, class_count: int, pretrained: bool):
    weights_name = {
        "efficientnet_b0": "EfficientNet_B0_Weights",
        "mobilenet_v3_small": "MobileNet_V3_Small_Weights",
        "resnet18": "ResNet18_Weights",
    }[architecture]
    weights = getattr(models, weights_name).DEFAULT if pretrained else None
    model = getattr(models, architecture)(weights=weights)
    if architecture == "efficientnet_b0":
        model.classifier[1] = nn.Linear(model.classifier[1].in_features, class_count)
    elif architecture == "mobilenet_v3_small":
        model.classifier[3] = nn.Linear(model.classifier[3].in_features, class_count)
    else:
        model.fc = nn.Linear(model.fc.in_features, class_count)
    return model


def train(manifest: Path, output: Path, epochs: int, batch_size: int, architecture: str, image_size: int, freeze_epochs: int, log_interval: int, log_file: Path, log_level: str, max_per_class: int, resume: bool) -> None:
    configure_logging(log_file, log_level)
    logger = logging.getLogger("smart-plant-care.training")
    try:
        import torch
        from PIL import Image
        from torch import nn
        from torch.utils.data import DataLoader, Dataset
        from torchvision import models, transforms
    except ImportError as exc:
        raise SystemExit("Training requires torch, torchvision and Pillow") from exc
    if epochs < 1 or freeze_epochs < 0 or freeze_epochs > epochs:
        raise SystemExit("epochs must be positive and freeze-epochs must be between 0 and epochs (inclusive)")
    if log_interval < 1:
        raise SystemExit("log-interval must be positive")
    if max_per_class < 0:
        raise SystemExit("max-per-class cannot be negative")
    random.seed(42)
    torch.manual_seed(42)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(42)
    rows = list(csv.DictReader(manifest.open(encoding="utf-8", newline="")))
    classes = sorted({row["label"] for row in rows})
    class_to_index = {label: index for index, label in enumerate(classes)}

    class PlantDataset(Dataset):
        def __init__(self, split: str):
            self.rows = [row for row in rows if row["split"] == split]
            if max_per_class:
                selected = []
                for label in classes:
                    class_rows = [row for row in self.rows if row["label"] == label]
                    random.Random(f"42:{split}:{label}").shuffle(class_rows)
                    selected.extend(class_rows[:max_per_class])
                self.rows = selected
            self.transform = transforms.Compose([
                transforms.Resize((image_size, image_size)),
                *([transforms.RandomHorizontalFlip(), transforms.RandomRotation(15), transforms.ColorJitter(0.15, 0.15, 0.12)] if split == "train" else []),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ])

        def __len__(self):
            return len(self.rows)

        def __getitem__(self, index):
            row = self.rows[index]
            with Image.open(row["path"]) as image:
                return self.transform(image.convert("RGB")), class_to_index[row["label"]]

    datasets = {split: PlantDataset(split) for split in ("train", "validation")}
    if not datasets["train"] or not datasets["validation"]:
        raise SystemExit("Manifest must contain non-empty train and validation splits")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    loaders = {
        "train": DataLoader(datasets["train"], batch_size=batch_size, shuffle=True, num_workers=0, pin_memory=device.type == "cuda"),
        "validation": DataLoader(datasets["validation"], batch_size=batch_size, shuffle=False, num_workers=0, pin_memory=device.type == "cuda"),
    }
    if resume:
        state_path = output.with_suffix(".pth")
        metadata_path = output.with_suffix(".metadata.json")
        if not state_path.is_file() or not metadata_path.is_file():
            raise SystemExit(f"Cannot resume: checkpoint or metadata is missing for {output}")
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        if metadata.get("architecture") != architecture or metadata.get("classes") != classes or metadata.get("image_size") != image_size:
            raise SystemExit("Cannot resume: architecture, manifest class mapping, or image size differs from checkpoint")
        start_epoch = int(metadata["epoch"])
        if start_epoch >= epochs:
            raise SystemExit(f"Checkpoint already reached epoch {start_epoch}; requested total epochs is {epochs}")
        model = make_model(torch, models, nn, architecture, len(classes), pretrained=False)
        checkpoint = torch.load(state_path, map_location="cpu", weights_only=True)
        model.load_state_dict(checkpoint["state_dict"])
        best_f1 = float(metadata.get("best_validation_macro_f1", -1.0))
        status_path = output.with_suffix(".training.json")
        previous = json.loads(status_path.read_text(encoding="utf-8")) if status_path.is_file() else {}
        history = list(previous.get("history", []))[:start_epoch]
        logger.info("checkpoint_resume_loaded checkpoint=%s completed_epochs=%s best_validation_macro_f1=%.6f", state_path.resolve(), start_epoch, best_f1)
    else:
        start_epoch = 0
        best_f1 = -1.0
        history: list[dict[str, float | int]] = []
        model = make_model(torch, models, nn, architecture, len(classes), pretrained=True)
    model = model.to(device)
    logger.info("training_started architecture=%s epochs=%s freeze_epochs=%s batch_size=%s image_size=%s device=%s cuda_available=%s torch=%s torchvision=%s cpu_threads=%s classes=%s train_images=%s validation_images=%s manifest=%s", architecture, epochs, freeze_epochs, batch_size, image_size, device, torch.cuda.is_available(), torch.__version__, __import__("torchvision").__version__, torch.get_num_threads(), len(classes), len(datasets["train"]), len(datasets["validation"]), manifest.resolve())
    if architecture == "efficientnet_b0":
        feature_parameters = list(model.features.parameters())
        head_parameters = list(model.classifier.parameters())
    elif architecture == "mobilenet_v3_small":
        feature_parameters = list(model.features.parameters())
        head_parameters = list(model.classifier.parameters())
    else:
        feature_parameters = list(model.layer1.parameters()) + list(model.layer2.parameters()) + list(model.layer3.parameters()) + list(model.layer4.parameters())
        head_parameters = list(model.fc.parameters())
    for parameter in feature_parameters:
        parameter.requires_grad = False
    optimizer = torch.optim.AdamW(head_parameters, lr=1e-3, weight_decay=1e-4)
    criterion = nn.CrossEntropyLoss(label_smoothing=0.05)
    started = time.time()
    output.parent.mkdir(parents=True, exist_ok=True)

    for epoch in range(start_epoch, epochs):
        epoch_started = time.time()
        if epoch == freeze_epochs:
            for parameter in feature_parameters:
                parameter.requires_grad = True
            optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4, weight_decay=1e-4)
        record: dict[str, float | int] = {"epoch": epoch + 1, "learning_rate": optimizer.param_groups[0]["lr"]}
        for split in ("train", "validation"):
            model.train(split == "train")
            loss_sum = correct = total = 0
            true_counts = [0] * len(classes)
            predicted_counts = [0] * len(classes)
            true_positive = [0] * len(classes)
            for batch_index, (images, targets) in enumerate(loaders[split], start=1):
                images, targets = images.to(device), targets.to(device)
                if split == "train":
                    optimizer.zero_grad(set_to_none=True)
                with torch.set_grad_enabled(split == "train"):
                    logits = model(images)
                    loss = criterion(logits, targets)
                    if split == "train":
                        loss.backward()
                        optimizer.step()
                predictions = logits.argmax(1)
                loss_sum += float(loss.detach()) * targets.size(0)
                correct += int((predictions == targets).sum())
                total += targets.size(0)
                for target, prediction in zip(targets.detach().cpu().tolist(), predictions.detach().cpu().tolist()):
                    true_counts[target] += 1
                    predicted_counts[prediction] += 1
                    if target == prediction:
                        true_positive[target] += 1
                if batch_index % log_interval == 0 or batch_index == len(loaders[split]):
                    elapsed = time.time() - epoch_started
                    batches_done = batch_index if split == "train" else len(loaders["train"]) + batch_index
                    batches_total = len(loaders["train"]) + len(loaders["validation"])
                    batches_per_second = batches_done / max(elapsed, 1e-6)
                    eta_seconds = (batches_total - batches_done) / max(batches_per_second, 1e-6)
                    logger.info("epoch_progress epoch=%s/%s split=%s batch=%s/%s samples=%s/%s running_loss=%.5f elapsed_seconds=%.1f eta_seconds=%.1f", epoch + 1, epochs, split, batch_index, len(loaders[split]), total, len(datasets[split]), loss_sum / max(total, 1), elapsed, eta_seconds)
            recalls = [tp / support if support else 0 for tp, support in zip(true_positive, true_counts)]
            precisions = [tp / predicted if predicted else 0 for tp, predicted in zip(true_positive, predicted_counts)]
            f1s = [2 * p * r / (p + r) if p + r else 0 for p, r in zip(precisions, recalls)]
            record[f"{split}_loss"] = loss_sum / max(total, 1)
            record[f"{split}_accuracy"] = correct / max(total, 1)
            record[f"{split}_macro_f1"] = sum(f1s) / len(f1s)
        history.append(record)
        logger.info("epoch_completed metrics=%s", json.dumps(record, ensure_ascii=False))
        # Preserve completed work if a long CPU run is interrupted before the
        # requested epoch count completes.
        output.with_suffix(".training.json").write_text(json.dumps({
            "history": history,
            "completed_epochs": len(history),
            "requested_epochs": epochs,
            "complete": False,
            "max_per_class": max_per_class,
            "train_images": len(datasets["train"]),
            "validation_images": len(datasets["validation"]),
            "seconds_this_resume": round(time.time() - started, 2),
            "resumed_from_epoch": start_epoch,
        }, indent=2), encoding="utf-8")
        val_f1 = float(record["validation_macro_f1"])
        if val_f1 > best_f1:
            best_f1 = val_f1
            model.cpu().eval()
            torch.jit.script(model).save(str(output))
            torch.save({"architecture": architecture, "state_dict": model.state_dict()}, output.with_suffix(".pth"))
            model.to(device)
            output.with_suffix(".labels.txt").write_text("\n".join(classes) + "\n", encoding="utf-8")
            output.with_suffix(".metadata.json").write_text(json.dumps({
                "architecture": architecture, "classes": classes, "image_size": image_size,
                "gradcam_layer": {"efficientnet_b0": "features.8", "mobilenet_v3_small": "features.12", "resnet18": "layer4"}[architecture],
                "normalization": {"mean": [0.485, 0.456, 0.406], "std": [0.229, 0.224, 0.225]},
                "pretrained": True, "best_validation_macro_f1": best_f1,
                "epoch": epoch + 1, "seed": 42, "manifest": str(manifest.resolve()),
                "max_per_class": max_per_class,
                "train_images": len(datasets["train"]),
                "validation_images": len(datasets["validation"]),
            }, indent=2), encoding="utf-8")
    output.with_suffix(".training.json").write_text(json.dumps({
        "history": history,
        "completed_epochs": len(history),
        "requested_epochs": epochs,
        "complete": True,
        "max_per_class": max_per_class,
        "train_images": len(datasets["train"]),
        "validation_images": len(datasets["validation"]),
        "seconds": round(time.time() - started, 2),
        "resumed_from_epoch": start_epoch,
    }, indent=2), encoding="utf-8")
    logger.info("training_completed best_validation_macro_f1=%.6f checkpoint=%s log=%s", best_f1, output.resolve(), log_file.resolve())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a transfer learning classifier; choose checkpoints on validation macro-F1.")
    parser.add_argument("--manifest", type=Path, required=True, help="CSV produced by prepare_training_data.py")
    parser.add_argument("--output", type=Path, default=Path("models/plant_health.pt"))
    parser.add_argument("--epochs", type=int, default=8)
    parser.add_argument("--freeze-epochs", type=int, default=2)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--image-size", type=int, default=224)
    parser.add_argument("--architecture", choices=["efficientnet_b0", "mobilenet_v3_small", "resnet18"], default="efficientnet_b0")
    parser.add_argument("--log-interval", type=int, default=50, help="Write progress after this many batches")
    parser.add_argument("--log-file", type=Path, default=Path("data/logs/training.log"))
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING"], default="INFO")
    parser.add_argument("--max-per-class", type=int, default=0, help="Deterministic per-class cap on train/validation for smoke runs; 0 means use all rows")
    parser.add_argument("--resume", action="store_true", help="Resume weights and epoch count from the existing output checkpoint")
    args = parser.parse_args()
    train(args.manifest, args.output, args.epochs, args.batch_size, args.architecture, args.image_size, args.freeze_epochs, args.log_interval, args.log_file, args.log_level, args.max_per_class, args.resume)
