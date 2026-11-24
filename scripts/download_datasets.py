from __future__ import annotations

import os
import hashlib
import json
import re
import subprocess
from pathlib import Path


DATASETS = {
    "plantvillage": "https://github.com/spMohanty/PlantVillage-Dataset.git",
    "plantdoc": "https://github.com/pratikkayal/PlantDoc-Dataset.git",
}


def _run_git(target: Path, *args: str, **kwargs: object) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(target), *args],
        check=True,
        **kwargs,
    )


def _windows_safe_paths(paths: list[bytes]) -> list[bytes]:
    safe: list[bytes] = []
    invalid_chars = set('<>:"/\\|?*')
    reserved_names = {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        *(f"COM{i}" for i in range(1, 10)),
        *(f"LPT{i}" for i in range(1, 10)),
    }
    for path_bytes in paths:
        path = path_bytes.decode("utf-8")
        parts = path.split("/")
        if (
            len(path) > 220
            or any(
                not part
                or part.endswith((" ", "."))
                or any(char in invalid_chars for char in part)
                or part.split(".")[0].upper() in reserved_names
                for part in parts
            )
        ):
            continue
        safe.append(path_bytes)
    return safe


def _checkout_plantdoc(target: Path) -> None:
    entries = _run_git(
        target,
        "ls-tree",
        "-r",
        "-z",
        "--long",
        "HEAD",
        stdout=subprocess.PIPE,
    ).stdout.split(b"\0")
    parsed: list[tuple[str, str, str]] = []
    for entry in entries:
        if not entry or b"\t" not in entry:
            continue
        metadata, path_bytes = entry.split(b"\t", 1)
        mode, kind, object_id, _size = metadata.decode("ascii").split(" ", 3)
        if kind == "blob":
            parsed.append((path_bytes.decode("utf-8"), object_id, mode))

    invalid_chars = set('<>:"/\\|?*')
    case_counts: dict[str, int] = {}
    for rel, _, _ in parsed:
        key = rel.casefold()
        case_counts[key] = case_counts.get(key, 0) + 1
    safe_paths: list[bytes] = []
    recovered: dict[str, str] = {}
    reserved_names = {
        "CON", "PRN", "AUX", "NUL",
        *(f"COM{i}" for i in range(1, 10)),
        *(f"LPT{i}" for i in range(1, 10)),
    }
    for rel, object_id, _mode in parsed:
        parts = rel.split("/")
        is_windows_safe = (
            len(rel) <= 220
            and all(part and not part.endswith((" ", ".")) for part in parts)
            and all(not any(char in invalid_chars for char in part) and part.split(".")[0].upper() not in reserved_names for part in parts)
            and case_counts[rel.casefold()] == 1
        )
        if is_windows_safe:
            safe_paths.append(rel.encode("utf-8"))
            continue

        # Preserve every Git blob even when NTFS cannot represent its original
        # name. Put recovered case-colliding/invalid entries under unique names.
        source = target / Path(*parts)
        if source.is_file() and case_counts[rel.casefold()] > 1:
            source.unlink()
        parent = Path(*parts[:-1])
        suffix = Path(parts[-1]).suffix
        stem = Path(parts[-1]).stem
        clean_stem = re.sub(r"[^A-Za-z0-9._-]+", "_", stem).strip(" ._") or "image"
        token = hashlib.sha256(rel.encode("utf-8")).hexdigest()[:10]
        local_rel = (parent / f"{clean_stem[:120]}__recovered_{token}{suffix.lower()}").as_posix()
        destination = target / Path(*local_rel.split("/"))
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not destination.exists():
            blob = _run_git(target, "cat-file", "blob", object_id, stdout=subprocess.PIPE).stdout
            destination.write_bytes(blob)
        recovered[rel] = local_rel

    if safe_paths:
        _run_git(
            target,
            "checkout-index",
            "--force",
            "--stdin",
            "-z",
            input=b"\0".join(safe_paths),
        )
    mapping_path = target.parent / "dataset_audit" / "plantdoc_filename_recovery.json"
    mapping_path.parent.mkdir(parents=True, exist_ok=True)
    mapping_path.write_text(json.dumps(recovered, indent=2, ensure_ascii=False), encoding="utf-8")
    image_count = sum(Path(rel).suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"} for rel, _, _ in parsed)
    print(f"PlantDoc Windows checkout: recovered {len(recovered)} Windows-incompatible tracked paths; {image_count} tracked images total.")


def _checkout_plantvillage(target: Path) -> None:
    paths = _run_git(
        target,
        "ls-tree",
        "-r",
        "-z",
        "--name-only",
        "HEAD",
        stdout=subprocess.PIPE,
    ).stdout.split(b"\0")
    safe_paths = _windows_safe_paths([path for path in paths if path])
    _run_git(
        target,
        "checkout-index",
        "--force",
        "--stdin",
        "-z",
        input=b"\0".join(safe_paths),
    )


def _is_git_repository(target: Path) -> bool:
    result = subprocess.run(
        ["git", "-C", str(target), "rev-parse", "--git-dir"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def _download(name: str, url: str, target: Path) -> None:
    if target.exists() and not _is_git_repository(target):
        remaining = [path for path in target.iterdir() if path.name != ".git"]
        if not remaining:
            git_dir = target / ".git"
            if git_dir.is_dir():
                git_dir.rmdir()
            else:
                git_dir.unlink(missing_ok=True)
            target.rmdir()
        else:
            raise RuntimeError(f"Target exists but is not a Git repository: {target}")
    if target.exists() and not (target / "README.md").exists():
        if name == "plantdoc" and os.name == "nt":
            _checkout_plantdoc(target)
        else:
            if name == "plantvillage":
                subprocess.run(
                    ["git", "-C", str(target), "fetch", "origin", "master", "--depth", "1"],
                    check=True,
                )
                subprocess.run(
                    ["git", "-C", str(target), "checkout", "-B", "master", "FETCH_HEAD"],
                    check=False,
                )
                if os.name == "nt":
                    _checkout_plantvillage(target)
                else:
                    _run_git(target, "checkout-index", "--force", "--all")
            else:
                _run_git(target, "checkout-index", "--force", "--all")
        return
    if target.exists() and not (target / ".git").exists():
        raise RuntimeError(f"Target exists but is not a Git repository: {target}")
    if not target.exists():
        if name == "plantdoc" and os.name == "nt":
            subprocess.run(
                ["git", "clone", "--depth", "1", "--no-checkout", url, str(target)],
                check=True,
            )
        else:
            subprocess.run(
                ["git", "clone", "--depth", "1", url, str(target)],
                check=True,
            )
    if name == "plantvillage":
        fetch = subprocess.run(
            ["git", "-C", str(target), "fetch", "origin", "master", "--depth", "1"],
            check=False,
        )
        if fetch.returncode == 0:
            subprocess.run(
                ["git", "-C", str(target), "checkout", "-B", "master", "FETCH_HEAD"],
                check=True,
            )
    if name == "plantdoc" and os.name == "nt":
        _checkout_plantdoc(target)


def main() -> None:
    root = Path(__file__).parents[1] / "data"
    root.mkdir(exist_ok=True)
    for name, url in DATASETS.items():
        target = root / name
        if target.exists() and (target / "README.md").exists():
            print(f"{name}: checking tracked files at {target}")
        print(f"Downloading {name}...")
        try:
            _download(name, url, target)
        except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
            raise SystemExit(
                f"Could not download {name}. Check network access and retry: {url}"
            ) from exc
    print("Datasets downloaded. Inspect each repository's README for its image layout.")


if __name__ == "__main__":
    main()
