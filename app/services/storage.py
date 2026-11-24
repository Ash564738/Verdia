from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Any


LOCAL_ROOT = Path(os.getenv("LOCAL_STORAGE_ROOT", Path(__file__).parents[2] / "data" / "uploads"))
STORAGE_BACKEND = os.getenv("STORAGE_BACKEND", "local").lower()
S3_BUCKET = os.getenv("S3_BUCKET", "")
S3_REGION = os.getenv("S3_REGION", "")
S3_ENDPOINT = os.getenv("S3_ENDPOINT", "")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY", "")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY", "")


def _s3_client() -> Any:
    try:
        import boto3
    except ImportError as exc:
        raise RuntimeError("S3_STORAGE requires boto3") from exc

    config: dict[str, Any] = {}
    if S3_REGION:
        config["region_name"] = S3_REGION
    if S3_ENDPOINT:
        config["endpoint_url"] = S3_ENDPOINT
    if S3_ACCESS_KEY and S3_SECRET_KEY:
        config["aws_access_key_id"] = S3_ACCESS_KEY
        config["aws_secret_access_key"] = S3_SECRET_KEY
    return boto3.client("s3", **config)


def save_private_image(payload: bytes, filename: str | None, user_id: str, category: str = "diagnoses") -> str:
    extension = Path(filename or "upload.jpg").suffix.lower()
    if extension not in {".jpg", ".jpeg", ".png", ".webp"}:
        extension = ".jpg"
    key = f"users/{user_id}/{category}/{uuid.uuid4()}{extension}"

    if STORAGE_BACKEND == "s3":
        if not S3_BUCKET:
            raise RuntimeError("S3_BUCKET is not configured")
        _s3_client().put_object(
            Bucket=S3_BUCKET,
            Key=key,
            Body=payload,
            ContentType={
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".webp": "image/webp",
            }.get(extension, "application/octet-stream"),
            ServerSideEncryption="AES256",
        )
        return key

    path = LOCAL_ROOT / key
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    return key


def delete_private_image(storage_key: str) -> None:
    if not storage_key:
        return
    if STORAGE_BACKEND == "s3":
        if S3_BUCKET:
            _s3_client().delete_object(Bucket=S3_BUCKET, Key=storage_key)
        return
    path = LOCAL_ROOT / storage_key
    if path.is_file():
        path.unlink()


def local_image_path(storage_key: str) -> Path | None:
    if STORAGE_BACKEND != "local":
        return None
    path = (LOCAL_ROOT / storage_key).resolve()
    root = LOCAL_ROOT.resolve()
    if path == root or root not in path.parents:
        return None
    return path if path.is_file() else None


def presigned_image_url(storage_key: str, expires_seconds: int = 900) -> str | None:
    if STORAGE_BACKEND != "s3" or not S3_BUCKET:
        return None
    return _s3_client().generate_presigned_url(
        "get_object",
        Params={"Bucket": S3_BUCKET, "Key": storage_key},
        ExpiresIn=expires_seconds,
    )
