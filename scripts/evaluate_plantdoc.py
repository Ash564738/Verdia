from __future__ import annotations

import argparse
import csv
import json
import random
from collections import defaultdict
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Cross-domain and unknown-class evaluation on held-out PlantDoc/test.")
    parser.add_argument("--checkpoint", type=Path, default=Path("models/plant_health.pt"))
    parser.add_argument("--validation-manifest", type=Path, default=Path("data/prepared/plantvillage/manifest.csv"))
    parser.add_argument("--plantdoc-root", type=Path, default=Path("data/plantdoc/test"))
    parser.add_argument("--mapping", type=Path, default=Path("ml/configs/plantdoc_label_mapping.json"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    import torch
    import numpy as np
    from PIL import Image
    from torch.utils.data import DataLoader, Dataset
    from torchvision import transforms

    metadata = json.loads(args.checkpoint.with_suffix(".metadata.json").read_text(encoding="utf-8"))
    classes = metadata["classes"]
    class_to_index = {name: index for index, name in enumerate(classes)}
    mapping = json.loads(args.mapping.read_text(encoding="utf-8"))["mapped"]
    audit_path = Path("data/dataset_audit/dataset_audit.json")
    excluded_test_paths: set[str] = set()
    if audit_path.exists():
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        for group in audit.get("plantdoc", {}).get("cross_split_duplicates", []):
            for relative in group:
                if relative.startswith("test/"):
                    excluded_test_paths.add((args.plantdoc_root.parent / relative).resolve().as_posix().lower())
    size = int(metadata.get("image_size", 224))
    transform = transforms.Compose([transforms.Resize((size, size)), transforms.ToTensor(), transforms.Normalize([.485, .456, .406], [.229, .224, .225])])
    model = torch.jit.load(str(args.checkpoint), map_location="cpu").eval()

    validation = [row for row in csv.DictReader(args.validation_manifest.open(encoding="utf-8", newline="")) if row["split"] == "validation" and row["label"] in class_to_index]
    class ValidationDataset(Dataset):
        def __len__(self): return len(validation)
        def __getitem__(self, index):
            row = validation[index]
            with Image.open(row["path"]) as image: return transform(image.convert("RGB"))
    validation_scores = []
    with torch.inference_mode():
        for images in DataLoader(ValidationDataset(), batch_size=32, num_workers=0):
            validation_scores.extend(model(images).softmax(1).max(1).values.tolist())
    if not validation_scores:
        raise SystemExit("Validation split is empty; threshold calibration must use validation data")
    # Validation-only threshold targeting a 5% in-domain rejection rate.
    threshold = float(np.quantile(validation_scores, 0.05))

    rows = []
    excluded_duplicates = 0
    for path in sorted(args.plantdoc_root.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
            if path.resolve().as_posix().lower() in excluded_test_paths:
                excluded_duplicates += 1
                continue
            source_label = path.parent.name
            mapped_label = mapping.get(source_label)
            rows.append((path, source_label, mapped_label))
    if not rows:
        raise SystemExit(f"No PlantDoc images found in {args.plantdoc_root}")

    y_true: list[int] = []
    y_pred: list[int] = []
    known_scores: list[float] = []
    unknown_scores: list[float] = []
    rejected_known = accepted_unknown = unknown_total = 0
    with torch.inference_mode():
        for path, source_label, mapped_label in rows:
            with Image.open(path) as image:
                probabilities = model(transform(image.convert("RGB")).unsqueeze(0)).softmax(1)[0]
            score = float(probabilities.max())
            prediction = int(probabilities.argmax())
            if mapped_label in class_to_index:
                y_true.append(class_to_index[mapped_label])
                y_pred.append(prediction)
                known_scores.append(score)
                rejected_known += int(score < threshold)
            else:
                unknown_scores.append(score)
                unknown_total += 1
                accepted_unknown += int(score >= threshold)
    class_metrics = {}
    confusion = [[0 for _ in classes] for _ in classes]
    for actual, predicted in zip(y_true, y_pred):
        confusion[actual][predicted] += 1
    f1_values = []
    correct = 0
    for label in sorted(set(y_true)):
        tp = sum(actual == label and predicted == label for actual, predicted in zip(y_true, y_pred))
        support = sum(actual == label for actual in y_true)
        predicted_count = sum(predicted == label for predicted in y_pred)
        precision = tp / predicted_count if predicted_count else 0.0
        recall = tp / support if support else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        name = classes[label]
        class_metrics[name] = {"precision": precision, "recall": recall, "f1": f1, "support": support}
        f1_values.append(f1)
        correct += tp
    auc_pairs = [(known, unknown) for known in known_scores for unknown in unknown_scores]
    auroc = sum(1.0 if known > unknown else 0.5 if known == unknown else 0.0 for known, unknown in auc_pairs) / len(auc_pairs) if auc_pairs else None
    rng = random.Random(42)
    bootstrap = []
    macro_f1_bootstrap = []
    if y_true:
        for _ in range(1000):
            sample = [rng.randrange(len(y_true)) for _ in y_true]
            bootstrap.append(sum(y_true[i] == y_pred[i] for i in sample) / len(sample))
            labels = set(y_true[i] for i in sample)
            sample_f1 = []
            for label in labels:
                tp = sum(y_true[i] == label and y_pred[i] == label for i in sample)
                support = sum(y_true[i] == label for i in sample)
                predicted_count = sum(y_pred[i] == label for i in sample)
                precision = tp / predicted_count if predicted_count else 0.0
                recall = tp / support if support else 0.0
                sample_f1.append(2 * precision * recall / (precision + recall) if precision + recall else 0.0)
            macro_f1_bootstrap.append(sum(sample_f1) / len(sample_f1))
    report = {
        "dataset": "PlantDoc official test",
        "threshold": threshold,
        "threshold_source": "PlantVillage validation fifth percentile; no PlantDoc test threshold tuning",
        "mapped_known_samples": len(y_true),
        "plantdoc_test_exact_duplicates_excluded": excluded_duplicates,
        "mapped_accuracy": correct / len(y_true) if y_true else None,
        "mapped_accuracy_95pct_bootstrap_ci": [float(np.quantile(bootstrap, .025)), float(np.quantile(bootstrap, .975))] if bootstrap else None,
        "mapped_macro_f1": sum(f1_values) / len(f1_values) if f1_values else None,
        "mapped_macro_f1_95pct_bootstrap_ci": [float(np.quantile(macro_f1_bootstrap, .025)), float(np.quantile(macro_f1_bootstrap, .975))] if macro_f1_bootstrap else None,
        "confusion_matrix": {"labels": classes, "matrix": confusion},
        "known_rejection_rate": rejected_known / len(known_scores) if known_scores else None,
        "unknown_samples": unknown_total,
        "unknown_acceptance_rate": accepted_unknown / unknown_total if unknown_total else None,
        "known_vs_unknown_max_softmax_auroc": auroc,
        "mapped_classes": class_metrics,
        "unmapped_source_classes": sorted({source_label for _, source_label, mapped_label in rows if not mapped_label}),
        "limitations": ["Unknown examples are PlantDoc leaf classes whose labels do not map safely to PlantVillage classes; this is not a non-leaf photo benchmark.", "Unmapped classes are treated as unknown rather than included in closed-set accuracy."],
    }
    output = args.output or args.checkpoint.with_suffix(".plantdoc-evaluation.json")
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    args.checkpoint.with_suffix(".threshold.json").write_text(json.dumps({
        "confidence_threshold": threshold,
        "method": "5th percentile of PlantVillage validation max-softmax confidence",
        "target_in_domain_rejection_rate": 0.05,
        "calibration_dataset": "PlantVillage validation",
        "ood_test_used_for_calibration": False,
    }, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
