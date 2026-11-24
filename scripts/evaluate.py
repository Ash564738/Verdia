from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a frozen checkpoint on a named held-out split.")
    parser.add_argument("--manifest", type=Path, required=True, help="Manifest produced by prepare_training_data.py")
    parser.add_argument("--split", choices=["test", "validation"], default="test")
    parser.add_argument("--checkpoint", type=Path, default=Path("models/plant_health.pt"))
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not args.checkpoint.exists():
        raise SystemExit(f"Checkpoint not found: {args.checkpoint}. Train a model first.")
    try:
        import torch
        from PIL import Image
        from torch.utils.data import DataLoader, Dataset
        from torchvision import transforms
    except ImportError as exc:
        raise SystemExit("Evaluation requires torch, torchvision and Pillow") from exc

    metadata_path = args.checkpoint.with_suffix(".metadata.json")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8")) if metadata_path.exists() else {}
    classes = metadata.get("classes") or [line.strip() for line in args.checkpoint.with_suffix(".labels.txt").read_text(encoding="utf-8").splitlines() if line.strip()]
    class_to_index = {name: index for index, name in enumerate(classes)}
    rows = [row for row in csv.DictReader(args.manifest.open(encoding="utf-8", newline="")) if row["split"] == args.split and row["label"] in class_to_index]
    if not rows:
        raise SystemExit(f"No compatible rows found for split={args.split}")
    size = int(metadata.get("image_size", 224))
    transform = transforms.Compose([
        transforms.Resize((size, size)), transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])

    class ManifestDataset(Dataset):
        def __len__(self):
            return len(rows)

        def __getitem__(self, index):
            row = rows[index]
            with Image.open(row["path"]) as image:
                return transform(image.convert("RGB")), class_to_index[row["label"]]

    model = torch.jit.load(str(args.checkpoint), map_location="cpu").eval()
    confusion = [[0 for _ in classes] for _ in classes]
    confidence_bins = [[0, 0.0, 0] for _ in range(15)]  # count, confidence sum, correct count
    top3_correct = total = 0
    with torch.inference_mode():
        for images, labels in DataLoader(ManifestDataset(), batch_size=args.batch_size, num_workers=0):
            probabilities = model(images).softmax(dim=1)
            confidence, predictions = probabilities.max(dim=1)
            top3 = probabilities.topk(min(3, len(classes)), dim=1).indices
            top3_correct += int((top3 == labels.unsqueeze(1)).any(dim=1).sum())
            total += labels.numel()
            for actual, predicted, score in zip(labels.tolist(), predictions.tolist(), confidence.tolist()):
                confusion[actual][predicted] += 1
                bucket = min(int(score * len(confidence_bins)), len(confidence_bins) - 1)
                confidence_bins[bucket][0] += 1
                confidence_bins[bucket][1] += score
                confidence_bins[bucket][2] += int(actual == predicted)

    per_class = {}
    precisions, recalls, f1s, weighted_f1s = [], [], [], []
    correct_total = 0
    for index, name in enumerate(classes):
        tp = confusion[index][index]
        support = sum(confusion[index])
        predicted = sum(confusion[actual][index] for actual in range(len(classes)))
        fp, fn = predicted - tp, support - tp
        precision = tp / predicted if predicted else 0.0
        recall = tp / support if support else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        per_class[name] = {"precision": precision, "recall": recall, "f1": f1, "support": support}
        precisions.append(precision); recalls.append(recall); f1s.append(f1); weighted_f1s.append(f1 * support)
        correct_total += tp
    ece = sum(abs(bin_correct / count - confidence_sum / count) * count for count, confidence_sum, bin_correct in confidence_bins if count) / max(total, 1)
    report = {
        "dataset": args.split,
        "samples": total,
        "accuracy": correct_total / max(total, 1),
        "top3_accuracy": top3_correct / max(total, 1),
        "macro_precision": sum(precisions) / len(precisions),
        "macro_recall": sum(recalls) / len(recalls),
        "macro_f1": sum(f1s) / len(f1s),
        "weighted_f1": sum(weighted_f1s) / max(total, 1),
        "expected_calibration_error_15_bins": ece,
        "confusion_matrix": {"labels": classes, "matrix": confusion},
        "per_class": per_class,
    }
    default_name = ".evaluation.json" if args.split == "test" else ".validation-evaluation.json"
    output = args.output or args.checkpoint.with_suffix(default_name)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
