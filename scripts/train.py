from __future__ import annotations

import argparse
import csv
import json
import random
import time
from collections import defaultdict
from pathlib import Path


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


def train(manifest: Path, output: Path, epochs: int, batch_size: int, architecture: str, image_size: int, freeze_epochs: int) -> None:
    try:
        import torch
        from PIL import Image
        from torch import nn
        from torch.utils.data import DataLoader, Dataset
        from torchvision import models, transforms
    except ImportError as exc:
        raise SystemExit("Training requires torch, torchvision and Pillow") from exc
    if epochs < 1 or freeze_epochs < 0 or freeze_epochs >= epochs:
        raise SystemExit("epochs must be positive and freeze-epochs must be smaller than epochs")
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
    model = make_model(torch, models, nn, architecture, len(classes), pretrained=True).to(device)
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
    best_f1 = -1.0
    history: list[dict[str, float | int]] = []
    started = time.time()
    output.parent.mkdir(parents=True, exist_ok=True)

    for epoch in range(epochs):
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
            for images, targets in loaders[split]:
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
            recalls = [tp / support if support else 0 for tp, support in zip(true_positive, true_counts)]
            precisions = [tp / predicted if predicted else 0 for tp, predicted in zip(true_positive, predicted_counts)]
            f1s = [2 * p * r / (p + r) if p + r else 0 for p, r in zip(precisions, recalls)]
            record[f"{split}_loss"] = loss_sum / max(total, 1)
            record[f"{split}_accuracy"] = correct / max(total, 1)
            record[f"{split}_macro_f1"] = sum(f1s) / len(f1s)
        history.append(record)
        print(json.dumps(record), flush=True)
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
            }, indent=2), encoding="utf-8")
    output.with_suffix(".training.json").write_text(json.dumps({"history": history, "seconds": round(time.time() - started, 2)}, indent=2), encoding="utf-8")
    print(f"Best validation macro-F1: {best_f1:.4f}; saved {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a transfer learning classifier; choose checkpoints on validation macro-F1.")
    parser.add_argument("--manifest", type=Path, required=True, help="CSV produced by prepare_training_data.py")
    parser.add_argument("--output", type=Path, default=Path("models/plant_health.pt"))
    parser.add_argument("--epochs", type=int, default=8)
    parser.add_argument("--freeze-epochs", type=int, default=2)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--image-size", type=int, default=224)
    parser.add_argument("--architecture", choices=["efficientnet_b0", "mobilenet_v3_small", "resnet18"], default="efficientnet_b0")
    args = parser.parse_args()
    train(args.manifest, args.output, args.epochs, args.batch_size, args.architecture, args.image_size, args.freeze_epochs)
