"""Create reproducible PlantVillage train/validation/test manifests.

The published color train/test split is preserved. Validation is sampled only
from official train and grouped by the image UUID (the leaf identifier used by
the repository's color export), so related views cannot cross train/validation.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import urllib.request
from collections import defaultdict
from pathlib import Path


SPLIT_URL = "https://huggingface.co/datasets/mohanty/PlantVillage/resolve/main/splits/color_{split}.txt"


def read_official_split(root: Path, split: str) -> list[Path]:
    url = SPLIT_URL.format(split=split)
    request = urllib.request.Request(url, headers={"User-Agent": "SmartPlantCareAI/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        paths = response.read().decode("utf-8").splitlines()
    result = [root / item.strip() for item in paths if item.strip()]
    missing = [str(path) for path in result if not path.is_file()]
    if missing:
        raise SystemExit(f"{len(missing)} files from official {split} split are missing; example: {missing[0]}")
    return result


def group_id(path: Path, label: str, leaf_map: dict[str, list[str]]) -> tuple[str, bool]:
    # Match the dataset publisher's image-identifier -> leaf_id mapping.
    identifier = path.name.split("___")[-1].split("copy")[0]
    for suffix in (".jpg", ".JPG", ".png", ".PNG"):
        identifier = identifier.replace(suffix, "")
    identifier = identifier.strip()
    suggestions = leaf_map.get(identifier.lower(), [])
    if len(suggestions) == 1:
        return suggestions[0], True
    for suggestion in suggestions:
        if label in suggestion:
            return suggestion, True
    return f"fallback_{identifier}", False


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-root", type=Path, default=Path("data/plantvillage"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/prepared/plantvillage"))
    parser.add_argument("--validation-fraction", type=float, default=0.1)
    args = parser.parse_args()
    if not 0 < args.validation_fraction < 0.5:
        raise SystemExit("validation-fraction must be between 0 and 0.5")

    official_train = read_official_split(args.dataset_root, "train")
    official_test = read_official_split(args.dataset_root, "test")
    leaf_map_path = args.dataset_root / "leaf_grouping" / "leaf-map.json"
    if not leaf_map_path.is_file():
        raise SystemExit(f"PlantVillage leaf identity metadata is missing: {leaf_map_path}")
    leaf_map = json.loads(leaf_map_path.read_text(encoding="utf-8"))
    audit_path = Path("data/dataset_audit/dataset_audit.json")
    duplicate_train_paths: set[str] = set()
    if audit_path.exists():
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        for group in audit.get("plantvillage_color", {}).get("duplicates", []):
            for relative in group:
                candidate = (args.dataset_root / "raw" / "color" / relative).resolve().as_posix()
                duplicate_train_paths.add(candidate)

    # Drop any official-train group that also occurs in official test. This
    # preserves the published test set and prevents the known fallback IDs from
    # leaking copies across the boundary.
    test_group_lookup = {str(path): group_id(path, path.parent.name, leaf_map)[0] for path in official_test}
    test_groups = {(path.parent.name, test_group_lookup[str(path)]) for path in official_test}
    # Deterministic group-level validation selection within each class.
    by_class: dict[str, dict[str, list[Path]]] = defaultdict(lambda: defaultdict(list))
    group_lookup: dict[str, tuple[str, bool]] = {}
    removed_train_overlap = 0
    removed_train_exact_duplicates = 0
    for path in official_train:
        identity = group_id(path, path.parent.name, leaf_map)
        group_lookup[str(path)] = identity
        if path.resolve().as_posix() in duplicate_train_paths:
            removed_train_exact_duplicates += 1
            continue
        if (path.parent.name, identity[0]) in test_groups:
            removed_train_overlap += 1
            continue
        by_class[path.parent.name][identity[0]].append(path)
    validation_groups: set[tuple[str, str]] = set()
    for class_name, groups in sorted(by_class.items()):
        ranked = sorted(
            groups,
            key=lambda group: hashlib.sha256(f"42:{class_name}:{group}".encode()).hexdigest(),
        )
        target = max(1, round(len(groups) * args.validation_fraction))
        validation_groups.update((class_name, group) for group in ranked[:target])

    rows: list[dict[str, str]] = []
    for path in official_train:
        group, matched = group_lookup[str(path)]
        if path.resolve().as_posix() in duplicate_train_paths:
            continue
        if (path.parent.name, group) in test_groups:
            continue
        split = "validation" if (path.parent.name, group) in validation_groups else "train"
        rows.append({"split": split, "path": path.resolve().as_posix(), "label": path.parent.name, "group_id": group, "group_source": "leaf-map" if matched else "fallback-image-identifier", "source": "PlantVillage-color"})
    for path in official_test:
        group, matched = group_id(path, path.parent.name, leaf_map)
        rows.append({"split": "test", "path": path.resolve().as_posix(), "label": path.parent.name, "group_id": group, "group_source": "leaf-map" if matched else "fallback-image-identifier", "source": "PlantVillage-color-official-test"})

    groups_by_split = {
        split: {(r["label"], r["group_id"]) for r in rows if r["split"] == split}
        for split in ("train", "validation", "test")
    }
    for left, right in (("train", "validation"), ("train", "test"), ("validation", "test")):
        overlap = groups_by_split[left] & groups_by_split[right]
        if overlap:
            raise SystemExit(f"Leaf group leakage detected between {left} and {right}: {len(overlap)} groups")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest = args.output_dir / "manifest.csv"
    with manifest.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=["split", "path", "label", "group_id", "group_source", "source"])
        writer.writeheader()
        writer.writerows(rows)
    counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for row in rows:
        counts[row["split"]][row["label"]] += 1
    summary = {split: {"images": sum(classes.values()), "classes": len(classes)} for split, classes in sorted(counts.items())}
    fallback_count = sum(row["group_source"] != "leaf-map" for row in rows)
    print(f"Manifest: {manifest}")
    print(f"Split summary: {summary}")
    print(f"Official-train rows quarantined due to leaf group overlap with official test: {removed_train_overlap}")
    print(f"Official-train exact duplicates quarantined: {removed_train_exact_duplicates}")
    print(f"Rows using fallback image identifiers because leaf-map has no exact leaf ID: {fallback_count}/{len(rows)}")
    print("Label list:", ", ".join(sorted(by_class)))


if __name__ == "__main__":
    main()
