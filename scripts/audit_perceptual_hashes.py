"""Compute pHash inventory and near-duplicate candidates for the Phase 1 sources.

No files are moved or excluded. Candidate pairs are reported for manual review;
the Hamming-distance cutoff is an audit heuristic, not a label or split rule.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import urllib.request
from collections import defaultdict
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).parents[1]
PV_SPLIT_REVISION = "9e97599868962bd0079b8db4b7f1efa9185fa1e7"
PV_SPLITS = f"https://huggingface.co/datasets/mohanty/PlantVillage/resolve/{PV_SPLIT_REVISION}/splits/color_{{split}}.txt"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def load_official_pv_paths(root: Path) -> tuple[dict[str, str], dict[str, str]]:
    mapping: dict[str, str] = {}
    split_sha256: dict[str, str] = {}
    for split in ("train", "test"):
        request = urllib.request.Request(PV_SPLITS.format(split=split), headers={"User-Agent": "SmartPlantCareAI/1.0"})
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = response.read()
        split_sha256[split] = hashlib.sha256(payload).hexdigest()
        relative_paths = payload.decode("utf-8").splitlines()
        for relative in relative_paths:
            relative = relative.strip()
            if not relative:
                continue
            path = (root / relative).resolve()
            if not path.is_file():
                raise SystemExit(f"Official PlantVillage path is missing locally: {path}")
            mapping[path.as_posix().lower()] = f"official_{split}"
    return mapping, split_sha256


def phash(image_path: Path) -> str:
    # Orthonormal 8x32 DCT basis; only low frequencies are retained.
    size, low = 32, 8
    x = np.arange(size, dtype=np.float64)
    k = np.arange(low, dtype=np.float64)[:, None]
    basis = np.cos(np.pi * (2 * x[None, :] + 1) * k / (2 * size))
    basis[0] *= np.sqrt(1 / size)
    basis[1:] *= np.sqrt(2 / size)
    with Image.open(image_path) as image:
        pixels = np.asarray(image.convert("L").resize((size, size), Image.Resampling.LANCZOS), dtype=np.float64)
    low_freq = basis @ pixels @ basis.T
    values = low_freq.flatten()
    median = np.median(values[1:])
    bits = values > median
    value = 0
    for bit in bits:
        value = (value << 1) | int(bit)
    return f"{value:016x}"


def find_candidates(records: list[dict[str, str]], max_distance: int) -> list[dict[str, object]]:
    buckets: dict[tuple[int, int], list[int]] = defaultdict(list)
    for index, record in enumerate(records):
        value = int(record["perceptual_hash"], 16)
        for band in range(4):
            buckets[(band, (value >> (16 * band)) & 0xFFFF)].append(index)
    pairs: set[tuple[int, int]] = set()
    for indices in buckets.values():
        if len(indices) < 2:
            continue
        for offset, left in enumerate(indices[:-1]):
            for right in indices[offset + 1:]:
                pairs.add((left, right))
    candidates = []
    for left, right in pairs:
        a, b = records[left], records[right]
        distance = (int(a["perceptual_hash"], 16) ^ int(b["perceptual_hash"], 16)).bit_count()
        if distance <= max_distance:
            candidates.append({
                "distance": distance,
                "dataset_a": a["dataset"], "path_a": a["path"], "label_a": a["original_label"], "split_a": a["split"],
                "dataset_b": b["dataset"], "path_b": b["path"], "label_b": b["original_label"], "split_b": b["split"],
                "exact_sha256_match": a["sha256"] == b["sha256"],
            })
    return sorted(candidates, key=lambda item: (item["distance"], item["dataset_a"], item["path_a"]))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plantvillage-root", type=Path, default=ROOT / "data" / "plantvillage")
    parser.add_argument("--plantdoc-root", type=Path, default=ROOT / "data" / "plantdoc")
    parser.add_argument("--audit-root", type=Path, default=ROOT / "data" / "dataset_audit")
    parser.add_argument("--max-hamming-distance", type=int, default=4)
    args = parser.parse_args()

    pv_paths, pv_split_sha256 = load_official_pv_paths(args.plantvillage_root)
    pv_root = (args.plantvillage_root / "raw" / "color").resolve()
    doc_root = args.plantdoc_root.resolve()
    records: list[dict[str, str]] = []
    source_versions = {
        "plantvillage": "7f7ecc7e1eaca78107e3affe7cb5abd9427e139a",
        "plantdoc": "5467f6012d78d1c446145d5f582da6096f852ae8",
    }
    licenses = {"plantvillage": "CC BY-SA 3.0 (upstream dataset card)", "plantdoc": "CC BY 4.0 (repository LICENSE.txt)"}

    for path in sorted(pv_root.rglob("*")):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
            records.append({
                "dataset": "PlantVillage-color", "source_version": source_versions["plantvillage"],
                "path": path.relative_to(pv_root).as_posix(), "original_label": path.parent.name,
                "split": pv_paths.get(path.resolve().as_posix().lower(), "not_in_official_split"),
                "license": licenses["plantvillage"], "quality_status": "valid",
            })
    for split in ("train", "test"):
        split_root = doc_root / split
        for path in sorted(split_root.rglob("*")):
            if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
                records.append({
                    "dataset": "PlantDoc", "source_version": source_versions["plantdoc"],
                    "path": path.relative_to(doc_root).as_posix(), "original_label": path.parent.name,
                    "split": split, "license": licenses["plantdoc"], "quality_status": "valid",
                })

    cache_path = args.audit_root / "phase1_perceptual_hash_cache.jsonl"
    cached: dict[str, dict[str, str]] = {}
    if cache_path.exists():
        for line in cache_path.read_text(encoding="utf-8").splitlines():
            item = json.loads(line)
            cached[f"{item['dataset']}:{item['path']}"] = item
    with cache_path.open("a", encoding="utf-8") as cache_stream:
      for index, record in enumerate(records, start=1):
        full_path = pv_root / record["path"] if record["dataset"] == "PlantVillage-color" else doc_root / record["path"]
        key = f"{record['dataset']}:{record['path']}"
        if key in cached:
            record.update({name: cached[key][name] for name in ("sha256", "perceptual_hash")})
            continue
        record["sha256"] = hashlib.sha256(full_path.read_bytes()).hexdigest()
        record["perceptual_hash"] = phash(full_path)
        cache_stream.write(json.dumps({"dataset": record["dataset"], "path": record["path"], "sha256": record["sha256"], "perceptual_hash": record["perceptual_hash"]}) + "\n")
        cache_stream.flush()
        if index % 5000 == 0:
            print(f"hashed {index}/{len(records)}", flush=True)

    pv_official = [record for record in records if record["dataset"] == "PlantVillage-color" and record["split"].startswith("official_")]
    pv_unassigned = [record["path"] for record in records if record["dataset"] == "PlantVillage-color" and record["split"] == "not_in_official_split"]
    split_counts = {name: sum(record["split"] == name for record in pv_official) for name in ("official_train", "official_test")}
    if len(pv_paths) != 54305 or len(pv_official) != 54305 or pv_unassigned or split_counts != {"official_train": 43596, "official_test": 10709}:
        raise SystemExit(f"PlantVillage official split coverage/count mismatch: paths={len(pv_paths)}, assigned={len(pv_official)}, split_counts={split_counts}, unassigned={len(pv_unassigned)}")

    candidates = find_candidates(records, args.max_hamming_distance)
    args.audit_root.mkdir(parents=True, exist_ok=True)
    manifest_path = args.audit_root / "phase1_perceptual_manifest.csv"
    fields = ["image_id", "image_path", "dataset", "source_version", "original_label", "split", "sha256", "perceptual_hash", "license", "quality_status"]
    with manifest_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for record in records:
            writer.writerow({**{key: value for key, value in record.items() if key != "path"}, "image_id": hashlib.sha256(f"{record['dataset']}:{record['path']}".encode()).hexdigest()[:20], "image_path": record["path"]})
    report = {
        "method": "8x8 low-frequency DCT pHash; candidate generation by four 16-bit bands",
        "max_hamming_distance": args.max_hamming_distance,
        "plantvillage_split_list_revision": PV_SPLIT_REVISION,
        "plantvillage_split_list_sha256": pv_split_sha256,
        "plantvillage_official_split_counts": split_counts,
        "plantvillage_official_split_coverage": "PASS (all 54,305 Color images assigned exactly once)",
        "candidate_pairs_require_manual_review": True,
        "dataset_counts": {name: sum(record["dataset"] == name for record in records) for name in sorted({record["dataset"] for record in records})},
        "candidate_pair_count": len(candidates),
        "cross_split_candidate_pair_count": sum(item["dataset_a"] == item["dataset_b"] and item["split_a"] != item["split_b"] for item in candidates),
        "cross_dataset_candidate_pair_count": sum(item["dataset_a"] != item["dataset_b"] for item in candidates),
        "candidates": candidates,
    }
    report_path = args.audit_root / "phase1_perceptual_hash_report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "candidates"}, indent=2, ensure_ascii=False))
    print(f"Manifest: {manifest_path}")
    print(f"Candidate report: {report_path}")


if __name__ == "__main__":
    main()
