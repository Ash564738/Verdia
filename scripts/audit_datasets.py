from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
import argparse

from PIL import Image, UnidentifiedImageError

ROOT = Path(__file__).parents[1]
OUTPUT = ROOT / "data" / "dataset_audit"
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def audit_folder(root: Path) -> dict:
    records = []
    invalid = []
    hashes: dict[str, list[str]] = defaultdict(list)
    class_counts: Counter[str] = Counter()
    modes: Counter[str] = Counter()
    sizes: Counter[str] = Counter()
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in IMAGE_SUFFIXES:
            continue
        relative = path.relative_to(root).as_posix()
        parts = relative.split("/")
        label = parts[-2] if len(parts) >= 2 else "unclassified"
        try:
            with Image.open(path) as image:
                width, height = image.size
                mode = image.mode
                image.verify()
            checksum = hashlib.sha256()
            with path.open("rb") as image_file:
                for chunk in iter(lambda: image_file.read(1024 * 1024), b""):
                    checksum.update(chunk)
            digest = checksum.hexdigest()
            record = {"path": relative, "label": label, "width": width, "height": height, "mode": mode, "sha256": digest}
            records.append(record)
            hashes[digest].append(relative)
            class_counts[label] += 1
            modes[mode] += 1
            sizes[f"{width}x{height}"] += 1
        except (OSError, UnidentifiedImageError, ValueError) as exc:
            invalid.append({"path": relative, "error": str(exc)})
    duplicate_groups = [paths for paths in hashes.values() if len(paths) > 1]
    cross_split_duplicates = [
        paths for paths in duplicate_groups
        if {Path(path).parts[0].lower() for path in paths if len(Path(path).parts) > 1} & {"train"}
        and {Path(path).parts[0].lower() for path in paths if len(Path(path).parts) > 1} & {"test"}
    ]
    return {
        "root": str(root), "valid_images": len(records), "invalid_images": invalid,
        "class_counts": dict(sorted(class_counts.items())), "class_count": len(class_counts),
        "mode_counts": dict(modes), "common_dimensions": dict(sizes.most_common(20)),
        "duplicates": duplicate_groups, "cross_split_duplicates": cross_split_duplicates,
        "manifest": records, "hashes": hashes,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the selected training sources, dimensions, color modes and exact duplicates.")
    parser.add_argument("--plantvillage-root", type=Path, default=ROOT / "data" / "plantvillage" / "raw" / "color")
    parser.add_argument("--plantdoc-root", type=Path, default=ROOT / "data" / "plantdoc")
    args = parser.parse_args()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    datasets = {
        "plantdoc": audit_folder(args.plantdoc_root),
        "plantvillage_color": audit_folder(args.plantvillage_root),
    }
    common_hashes = set(datasets["plantdoc"]["hashes"]) & set(datasets["plantvillage_color"]["hashes"])
    cross_dataset_duplicates = [
        {"sha256": digest, "plantdoc": datasets["plantdoc"]["hashes"][digest], "plantvillage_color": datasets["plantvillage_color"]["hashes"][digest]}
        for digest in sorted(common_hashes)
    ]
    report = {
        name: {key: value for key, value in audit.items() if key not in {"manifest", "hashes"}}
        for name, audit in datasets.items()
    }
    report["cross_dataset_duplicates"] = cross_dataset_duplicates
    (OUTPUT / "dataset_audit.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    for name, audit in datasets.items():
        filename = "plantvillage_manifest.csv" if name == "plantvillage_color" else f"{name}_manifest.csv"
        with (OUTPUT / filename).open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=["path", "label", "width", "height", "mode", "sha256"])
            writer.writeheader()
            writer.writerows(audit["manifest"])
    print(json.dumps({"plantdoc": report["plantdoc"], "plantvillage_color": report["plantvillage_color"], "cross_dataset_duplicate_groups": len(cross_dataset_duplicates)}, indent=2, ensure_ascii=False)[:12000])


if __name__ == "__main__":
    main()
