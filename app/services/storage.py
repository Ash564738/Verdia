from __future__ import annotations

import logging
import os
import uuid
from functools import lru_cache
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from botocore.config import Config

from app.config import APP_ENV

logger = logging.getLogger("smart-plant-care.storage")

STORAGE_BACKEND = os.getenv("STORAGE_BACKEND", "").strip().lower()
S3_BUCKET = os.getenv("S3_BUCKET", "").strip()
S3_REGION = os.getenv("S3_REGION", "").strip()
S3_ENDPOINT = os.getenv("S3_ENDPOINT", "").strip().rstrip("/")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY", "").strip()
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY", "").strip()


def storage_configuration_errors() -> list[str]:
    """Return safe-to-display configuration errors without exposing credentials."""
    if APP_ENV == "test":
        return []
    errors: list[str] = []
    if STORAGE_BACKEND != "s3":
        errors.append("STORAGE_BACKEND must be 's3'; local user-upload storage is disabled")
    if not S3_BUCKET:
        errors.append("S3_BUCKET is empty; create a private Supabase Storage bucket and set its name")
    if not S3_REGION:
        errors.append("S3_REGION is empty; copy the region from Supabase Storage S3 settings")
    endpoint = urlsplit(S3_ENDPOINT)
    if endpoint.scheme != "https" or not endpoint.netloc or "/storage/v1/s3" not in endpoint.path:
        errors.append("S3_ENDPOINT must be the HTTPS S3 endpoint shown in Supabase Storage settings")
    if not S3_ACCESS_KEY or not S3_SECRET_KEY:
        errors.append("Supabase S3_ACCESS_KEY and S3_SECRET_KEY are required")
    return errors


@lru_cache(maxsize=1)
def _s3_client() -> Any:
    errors = storage_configuration_errors()
    if errors:
        raise RuntimeError("; ".join(errors))
    try:
        import boto3
    except ImportError as exc:
        raise RuntimeError("S3 storage requires boto3; install requirements.txt") from exc
    return boto3.client(
        "s3",
        endpoint_url=S3_ENDPOINT,
        region_name=S3_REGION,
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
        config=Config(signature_version="s3v4", s3={"addressing_style": "path"}, retries={"max_attempts": 3}),
    )


def check_storage_ready() -> None:
    """Fail startup unless the configured private Supabase bucket is reachable."""
    errors = storage_configuration_errors()
    if errors:
        logger.error("storage_configuration_invalid errors=%s", errors)
        raise RuntimeError("Supabase Storage configuration is invalid: " + " | ".join(errors))
    if APP_ENV == "test":
        logger.info("storage_startup_check_skipped environment=test")
        return
    endpoint_host = urlsplit(S3_ENDPOINT).netloc
    logger.info("supabase_storage_check_started bucket=%s endpoint_host=%s region=%s", S3_BUCKET, endpoint_host, S3_REGION)
    try:
        _s3_client().head_bucket(Bucket=S3_BUCKET)
    except Exception as exc:
        logger.exception("supabase_storage_check_failed bucket=%s endpoint_host=%s", S3_BUCKET, endpoint_host)
        raise RuntimeError("Supabase Storage bucket check failed; verify bucket name, S3 endpoint, region, and rotated S3 keys") from exc
    logger.info("supabase_storage_check_succeeded bucket=%s endpoint_host=%s", S3_BUCKET, endpoint_host)


def save_private_image(
    payload: bytes,
    filename: str | None,
    user_id: str,
    category: str = "diagnoses",
    request_id: str = "-",
) -> str:
    errors = storage_configuration_errors()
    if errors:
        logger.error("image_storage_rejected request_id=%s backend=%s errors=%s", request_id, STORAGE_BACKEND or "unset", errors)
        raise RuntimeError("Supabase Storage is not configured: " + "; ".join(errors))
    if APP_ENV == "test":
        raise RuntimeError("User-upload image storage is disabled in tests")

    extension = Path(filename or "upload.jpg").suffix.lower()
    if extension not in {".jpg", ".jpeg", ".png", ".webp"}:
        extension = ".jpg"
    safe_category = "/".join(part for part in category.split("/") if part and part not in {".", ".."})
    key = f"users/{user_id}/{safe_category}/{uuid.uuid4()}{extension}"
    content_type = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
    }[extension]
    logger.info(
        "supabase_image_upload_started request_id=%s bucket=%s user_id=%s category=%s bytes=%s content_type=%s",
        request_id, S3_BUCKET, user_id, safe_category, len(payload), content_type,
    )
    try:
        # Supabase Storage S3 does not support x-amz-server-side-encryption.
        _s3_client().put_object(Bucket=S3_BUCKET, Key=key, Body=payload, ContentType=content_type)
    except Exception as exc:
        logger.exception(
            "supabase_image_upload_failed request_id=%s bucket=%s user_id=%s bytes=%s",
            request_id, S3_BUCKET, user_id, len(payload),
        )
        raise RuntimeError("Image upload to Supabase Storage failed; check backend.log and storage key/bucket settings") from exc
    logger.info("supabase_image_upload_succeeded request_id=%s bucket=%s user_id=%s object_id=%s", request_id, S3_BUCKET, user_id, key.rsplit("/", 1)[-1])
    return key


def delete_private_image(storage_key: str, request_id: str = "-") -> None:
    if not storage_key:
        return
    if APP_ENV == "test":
        raise RuntimeError("User-upload image storage is disabled in tests")
    errors = storage_configuration_errors()
    if errors:
        raise RuntimeError("Supabase Storage is not configured: " + "; ".join(errors))
    try:
        _s3_client().delete_object(Bucket=S3_BUCKET, Key=storage_key)
    except Exception:
        logger.exception("supabase_image_delete_failed request_id=%s bucket=%s object_id=%s", request_id, S3_BUCKET, storage_key.rsplit("/", 1)[-1])
        raise
    logger.info("supabase_image_delete_succeeded request_id=%s bucket=%s object_id=%s", request_id, S3_BUCKET, storage_key.rsplit("/", 1)[-1])


def local_image_path(storage_key: str) -> None:
    """Local image storage is intentionally disabled; private images live in Supabase."""
    return None


def presigned_image_url(storage_key: str, expires_seconds: int = 900) -> str | None:
    if APP_ENV == "test" or storage_configuration_errors():
        return None
    try:
        return _s3_client().generate_presigned_url(
            "get_object",
            Params={"Bucket": S3_BUCKET, "Key": storage_key},
            ExpiresIn=expires_seconds,
        )
    except Exception:
        logger.exception("supabase_presign_failed bucket=%s object_id=%s", S3_BUCKET, storage_key.rsplit("/", 1)[-1])
        raise
