from __future__ import annotations

import io
import os
import logging
import secrets
import time
import uuid
import unicodedata
from pathlib import Path
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any

from fastapi import Depends, FastAPI, File, HTTPException, Query, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from PIL import Image, ImageStat, UnidentifiedImageError
from pydantic import BaseModel, Field

from app.security import create_token, decode_token, hash_password, verify_password
from app.services.diagnosis import DiagnosisService
from app.services.qa import EnglishPlantQA
from app.services.storage import delete_private_image, local_image_path, presigned_image_url, save_private_image
from app.storage import connection, decode_json, init_db, row_dict


logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("smart-plant-care")
log_dir = Path(__file__).parents[1] / "data" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
file_handler = logging.FileHandler(log_dir / "backend.log", encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
logging.getLogger().addHandler(file_handler)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


class RegisterRequest(BaseModel):
    email: str
    password: str = Field(min_length=8, max_length=128)
    name: str = Field(min_length=1, max_length=120)


class LoginRequest(BaseModel):
    email: str
    password: str


class ProfileUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=120)


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8, max_length=128)


class PasswordResetRequest(BaseModel):
    email: str


class PasswordResetConfirmRequest(BaseModel):
    email: str
    token: str
    new_password: str = Field(min_length=8, max_length=128)


class PlantRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    species: str = Field(min_length=1, max_length=120)
    variety: str | None = None
    started_at: str | None = None
    location: str | None = None
    notes: str | None = None
    image_path: str | None = None


SUPPORTED_PLANT_SPECIES = [
    {"id": "Apple", "name": "Táo", "name_en": "Apple"},
    {"id": "Bell pepper", "name": "Ớt chuông", "name_en": "Bell pepper"},
    {"id": "Blueberry", "name": "Việt quất", "name_en": "Blueberry"},
    {"id": "Cherry", "name": "Anh đào", "name_en": "Cherry"},
    {"id": "Corn", "name": "Ngô", "name_en": "Corn"},
    {"id": "Grape", "name": "Nho", "name_en": "Grape"},
    {"id": "Orange", "name": "Cam", "name_en": "Orange"},
    {"id": "Peach", "name": "Đào", "name_en": "Peach"},
    {"id": "Potato", "name": "Khoai tây", "name_en": "Potato"},
    {"id": "Raspberry", "name": "Mâm xôi", "name_en": "Raspberry"},
    {"id": "Soybean", "name": "Đậu nành", "name_en": "Soybean"},
    {"id": "Squash", "name": "Bí", "name_en": "Squash"},
    {"id": "Strawberry", "name": "Dâu tây", "name_en": "Strawberry"},
    {"id": "Tomato", "name": "Cà chua", "name_en": "Tomato"},
]


class CareRequest(BaseModel):
    plant_id: str | None = None
    kind: str = Field(min_length=1, max_length=80)
    note: str | None = None
    occurred_at: str | None = None


class ReminderRequest(BaseModel):
    plant_id: str | None = None
    kind: str = Field(min_length=1, max_length=80)
    due_at: str
    note: str | None = None


class ReminderCompleteRequest(BaseModel):
    completed: bool = True


class FeedbackRequest(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str | None = Field(default=None, max_length=1000)


class QuestionRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)


class DiseaseRequest(BaseModel):
    code: str
    plant: str
    name: str
    name_vi: str
    pathogen: str = ""
    symptoms: str
    conditions: str
    treatment: str
    prevention: str
    image_url: str | None = None


class ModelRequest(BaseModel):
    name: str
    version: str
    architecture: str = "mobilenet_v3_small"
    dataset_version: str = "plantdoc+plantvillage"
    class_count: int = 0
    weights_path: str = "models/plant_health.pt"
    preprocessing_config: dict[str, Any] = {}
    threshold_config: dict[str, Any] = {}
    status: str = "registered"
    metrics: dict[str, Any] = {}


bearer = HTTPBearer(auto_error=False)
diagnosis_service = DiagnosisService()
qa_service = EnglishPlantQA()
diagnosis_service.load()
password_reset_tokens: dict[str, tuple[str, float]] = {}


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    diagnosis_service.load()
    yield


app = FastAPI(title="Smart Plant Care AI API", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("unhandled_exception method=%s path=%s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

rate_limits: dict[str, list[float]] = {}


@app.middleware("http")
async def rate_limit(request: Request, call_next):
    path = request.url.path
    protected = path.startswith("/api/v1/auth/login") or path.startswith("/api/v1/auth/register") or "diagnoses/predict" in path or path.endswith("/api/v1/diagnose")
    if protected:
        client = request.client.host if request.client else "unknown"
        key = f"{client}:{path}"
        now_time = time.time()
        entries = [timestamp for timestamp in rate_limits.get(key, []) if now_time - timestamp < 60]
        limit = 10 if "/auth/" in path else 30
        if len(entries) >= limit:
            raise HTTPException(429, "Too many requests. Please wait before retrying.")
        entries.append(now_time)
        rate_limits[key] = entries
    return await call_next(request)


@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    return {"message": "Smart Plant Care AI API", "docs": "/docs", "health": "/health"}


def current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)) -> dict[str, Any]:
    if not credentials:
        raise HTTPException(401, "Authentication required")
    try:
        claims = decode_token(credentials.credentials)
    except (ValueError, KeyError, TypeError, UnicodeDecodeError) as exc:
        raise HTTPException(401, "Invalid or expired token") from exc
    with connection() as db:
        user = row_dict(db.execute("SELECT id,email,name,role,is_active,created_at FROM users WHERE id=?", (claims["sub"],)).fetchone())
    if not user or not user["is_active"]:
        raise HTTPException(401, "Account is inactive")
    return user


def admin_user(user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    if user["role"] != "ADMIN":
        raise HTTPException(403, "Administrator access required")
    return user


def owned(db: Any, table: str, item_id: str, user_id: str) -> dict[str, Any]:
    row = row_dict(db.execute(f"SELECT * FROM {table} WHERE id=? AND user_id=?", (item_id, user_id)).fetchone())
    if not row:
        raise HTTPException(404, "Resource not found")
    return row


def audit(db: Any, actor_id: str, action: str, target_type: str, target_id: str | None = None, details: dict[str, Any] | None = None) -> None:
    db.execute(
        "INSERT INTO audit_logs (id,actor_id,action,target_type,target_id,details,created_at) VALUES (?,?,?,?,?,?,?)",
        (str(uuid.uuid4()), actor_id, action, target_type, target_id, __import__("json").dumps(details or {}), now()),
    )


@app.get("/health")
def health() -> dict[str, str]:
    logger.info("health_check model=%s", diagnosis_service.model_status)
    with connection() as db:
        db.execute("SELECT 1")
    return {"status": "ok", "model": diagnosis_service.model_status, "database": "ok"}


@app.post("/api/v1/auth/register", status_code=201)
def register(payload: RegisterRequest) -> dict[str, Any]:
    with connection() as db:
        if db.execute("SELECT 1 FROM users WHERE email=?", (payload.email.lower(),)).fetchone():
            raise HTTPException(409, "Email is already registered")
        user_id = str(uuid.uuid4())
        db.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?)", (user_id, payload.email.lower(), hash_password(payload.password), payload.name, "USER", True, now()))
    logger.info("user_registered user_id=%s email=%s", user_id, payload.email.lower())
    return {"user": {"id": user_id, "email": payload.email.lower(), "name": payload.name, "role": "USER"}, "access_token": create_token(user_id, "USER"), "token_type": "bearer"}


@app.post("/api/v1/auth/login")
def login(payload: LoginRequest) -> dict[str, Any]:
    with connection() as db:
        user = row_dict(db.execute("SELECT * FROM users WHERE email=?", (payload.email.lower(),)).fetchone())
    if not user or not user["is_active"] or not verify_password(payload.password, user["password_hash"]):
        logger.warning("login_failed email=%s", payload.email)
        raise HTTPException(401, "Invalid email or password")
    logger.info("login_success user_id=%s", user["id"])
    return {"access_token": create_token(user["id"], user["role"]), "refresh_token": create_token(user["id"], user["role"], 604800), "token_type": "bearer"}


@app.post("/api/v1/auth/logout")
def logout(_: dict[str, Any] = Depends(current_user)) -> dict[str, str]:
    return {"message": "Logged out"}


@app.post("/api/v1/auth/refresh")
def refresh(user: dict[str, Any] = Depends(current_user)) -> dict[str, str]:
    return {"access_token": create_token(user["id"], user["role"]), "token_type": "bearer"}


@app.get("/api/v1/auth/me")
def me(user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    return user


@app.put("/api/v1/auth/me")
def update_me(payload: ProfileUpdate, user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    with connection() as db:
        db.execute("UPDATE users SET name=? WHERE id=?", (payload.name, user["id"]))
    return {**user, "name": payload.name}


@app.put("/api/v1/auth/password")
def change_password(payload: PasswordChangeRequest, user: dict[str, Any] = Depends(current_user)) -> dict[str, str]:
    with connection() as db:
        account = row_dict(db.execute("SELECT password_hash FROM users WHERE id=?", (user["id"],)).fetchone())
        if not account or not verify_password(payload.current_password, account["password_hash"]):
            raise HTTPException(400, "Current password is incorrect")
        db.execute("UPDATE users SET password_hash=? WHERE id=?", (hash_password(payload.new_password), user["id"]))
    return {"message": "Password changed"}


@app.post("/api/v1/auth/forgot-password")
def forgot_password(payload: PasswordResetRequest) -> dict[str, str]:
    token = secrets.token_urlsafe(32)
    with connection() as db:
        user = db.execute("SELECT id FROM users WHERE email=?", (payload.email.lower(),)).fetchone()
    if user:
        password_reset_tokens[payload.email.lower()] = (token, time.time() + 900)
        return {"message": "Password reset token created", "reset_token": token}
    return {"message": "If the account exists, password reset instructions will be sent"}


@app.post("/api/v1/auth/reset-password")
def reset_password(payload: PasswordResetConfirmRequest) -> dict[str, str]:
    reset = password_reset_tokens.pop(payload.email.lower(), None)
    if not reset or reset[1] < time.time() or not secrets.compare_digest(reset[0], payload.token):
        raise HTTPException(400, "Reset token is invalid or expired")
    with connection() as db:
        user = row_dict(db.execute("SELECT id FROM users WHERE email=?", (payload.email.lower(),)).fetchone())
        if not user:
            raise HTTPException(404, "Account not found")
        db.execute("UPDATE users SET password_hash=? WHERE id=?", (hash_password(payload.new_password), user["id"]))
    return {"message": "Password reset"}


@app.get("/api/v1/plants")
def plants_catalog() -> list[dict[str, Any]]:
    return SUPPORTED_PLANT_SPECIES


@app.get("/api/v1/plants/{plant_id}")
def plant_catalog_detail(plant_id: str) -> dict[str, Any]:
    item = next((p for p in plants_catalog() if p["id"].lower() == plant_id.lower() or p["name"].lower() == plant_id.lower()), None)
    if not item:
        raise HTTPException(404, "Plant type not found")
    return item


@app.post("/api/v1/my-plants", status_code=201)
def create_plant(payload: PlantRequest, user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    allowed = {item["id"].lower() for item in SUPPORTED_PLANT_SPECIES}
    if payload.species.lower() not in allowed:
        raise HTTPException(422, "Loài cây chưa nằm trong 13 loài đã huấn luyện")
    item_id = str(uuid.uuid4())
    with connection() as db:
        db.execute("INSERT INTO plants VALUES (?,?,?,?,?,?,?,?,?,?,?)", (item_id, user["id"], payload.name, payload.species, payload.variety, payload.started_at, payload.location, payload.notes, payload.image_path, "active", now()))
    return {"id": item_id, "user_id": user["id"], **payload.model_dump(), "status": "active"}


@app.get("/api/v1/my-plants")
def list_plants(user: dict[str, Any] = Depends(current_user)) -> list[dict[str, Any]]:
    with connection() as db:
        return [dict(row) for row in db.execute("SELECT * FROM plants WHERE user_id=? ORDER BY created_at DESC", (user["id"],))]


@app.get("/api/v1/my-plants/{plant_id}")
def get_plant(plant_id: str, user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    with connection() as db:
        return owned(db, "plants", plant_id, user["id"])


@app.put("/api/v1/my-plants/{plant_id}")
def update_plant(plant_id: str, payload: PlantRequest, user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    allowed = {item["id"].lower() for item in SUPPORTED_PLANT_SPECIES}
    if payload.species.lower() not in allowed:
        raise HTTPException(422, "Loài cây chưa nằm trong 13 loài đã huấn luyện")
    with connection() as db:
        owned(db, "plants", plant_id, user["id"])
        db.execute("UPDATE plants SET name=?,species=?,variety=?,started_at=?,location=?,notes=?,image_path=? WHERE id=?", (*payload.model_dump().values(), plant_id))
        return owned(db, "plants", plant_id, user["id"])


@app.delete("/api/v1/my-plants/{plant_id}")
def delete_plant(plant_id: str, user: dict[str, Any] = Depends(current_user)) -> dict[str, str]:
    with connection() as db:
        owned(db, "plants", plant_id, user["id"])
        db.execute("DELETE FROM plants WHERE id=?", (plant_id,))
    return {"message": "Plant deleted"}


@app.post("/api/v1/my-plants/{plant_id}/image")
async def upload_plant_image(plant_id: str, file: UploadFile = File(...), user: dict[str, Any] = Depends(current_user)) -> dict[str, str]:
    if file.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(415, "Only JPEG, PNG, and WebP images are supported")
    payload = await file.read()
    if len(payload) > 10 * 1024 * 1024:
        raise HTTPException(413, "Image must be smaller than 10 MB")
    validate_image(payload)
    key = save_private_image(payload, file.filename, user["id"], f"plants/{plant_id}")
    with connection() as db:
        owned(db, "plants", plant_id, user["id"])
        db.execute("UPDATE plants SET image_path=? WHERE id=?", (key, plant_id))
    return {"storage_key": key}


@app.get("/api/v1/my-plants/{plant_id}/image")
def plant_image(plant_id: str, user: dict[str, Any] = Depends(current_user)) -> Response:
    with connection() as db:
        plant = owned(db, "plants", plant_id, user["id"])
    key = plant.get("image_path")
    if not key:
        raise HTTPException(404, "Plant image not found")
    local_path = local_image_path(key)
    if local_path:
        return FileResponse(local_path)
    signed = presigned_image_url(key)
    if signed:
        return RedirectResponse(signed)
    raise HTTPException(404, "Private image storage is unavailable")


def validate_image(payload: bytes) -> Image.Image:
    try:
        image = Image.open(io.BytesIO(payload))
        image.verify()
        image = Image.open(io.BytesIO(payload)).convert("RGB")
    except (UnidentifiedImageError, OSError) as exc:
        raise HTTPException(400, "The uploaded file is not a valid image") from exc
    if image.width < 32 or image.height < 32:
        raise HTTPException(400, "Image dimensions must be at least 32x32 pixels")
    stats = ImageStat.Stat(image)
    if max(stats.mean) < 15:
        raise HTTPException(422, "Image is too dark; please take another photo")
    if max(stats.var) < 80:
        raise HTTPException(422, "Image appears too blurry or uniform; please take another photo")
    pixels = image.resize((64, 64)).getdata()
    green_pixels = sum(1 for r, g, b in pixels if g > r * 1.05 and g > b * 1.05)
    if green_pixels / 4096 < 0.05:
        raise HTTPException(422, "Leaf area is too small or image does not appear to show a plant leaf")
    return image




@app.post("/api/v1/diagnose")
async def diagnose(file: UploadFile = File(...), user: dict[str, Any] | None = Depends(lambda: None)) -> dict[str, Any]:
    if file.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(415, "Only JPEG, PNG, and WebP images are supported")
    payload = await file.read()
    if len(payload) > 10 * 1024 * 1024:
        raise HTTPException(413, "Image must be smaller than 10 MB")
    image = validate_image(payload)
    try:
        diagnosis_service.require_model()
    except RuntimeError as exc:
        raise HTTPException(503, str(exc)) from exc
    result = diagnosis_service.predict(image)
    return {"filename": file.filename, **result}


@app.post("/api/v1/diagnoses/predict")
async def predict(file: UploadFile = File(...), plant_id: str | None = None, note: str | None = None, user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    if file.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(415, "Only JPEG, PNG, and WebP images are supported")
    payload = await file.read()
    if len(payload) > 10 * 1024 * 1024:
        raise HTTPException(413, "Image must be smaller than 10 MB")
    image = validate_image(payload)
    try:
        diagnosis_service.require_model()
    except RuntimeError as exc:
        raise HTTPException(503, str(exc)) from exc
    result = diagnosis_service.predict(image)
    saved_image = save_private_image(payload, file.filename, user["id"], "diagnoses")
    diagnosis_id = str(uuid.uuid4())
    with connection() as db:
        if plant_id:
            owned(db, "plants", plant_id, user["id"])
        prediction = result.get("prediction") or {}
        top_predictions = prediction.get("top_predictions", [])
        db.execute(
            "INSERT INTO diagnoses VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                diagnosis_id,
                user["id"],
                plant_id,
                file.filename,
                saved_image,
                result["plant"]["name"],
                result["disease"]["code"],
                result["status"],
                float(prediction.get("confidence", result["confidence"])),
                __import__("json").dumps(top_predictions),
                result["recommendation"],
                result["model"]["version"],
                result["severity"],
                note,
                now(),
            ),
        )
        db.execute(
            "INSERT INTO diagnosis_images (id,diagnosis_id,user_id,storage_key,filename,created_at) VALUES (?,?,?,?,?,?)",
            (str(uuid.uuid4()), diagnosis_id, user["id"], saved_image, file.filename, now()),
        )
        for rank, item in enumerate(top_predictions, start=1):
            db.execute(
                "INSERT INTO scan_predictions (id,diagnosis_id,class_code,class_name,confidence,rank,created_at) VALUES (?,?,?,?,?,?,?)",
                (
                    str(uuid.uuid4()),
                    diagnosis_id,
                    item["class"],
                    item["class"],
                    float(item["confidence"]),
                    rank,
                    now(),
                ),
            )
    return {"id": diagnosis_id, **result, "created_at": now()}


@app.get("/api/v1/diagnoses")
def list_diagnoses(status: str | None = None, plant_id: str | None = None, user: dict[str, Any] = Depends(current_user)) -> list[dict[str, Any]]:
    query, params = "SELECT * FROM diagnoses WHERE user_id=?", [user["id"]]
    if status:
        query += " AND status=?"; params.append(status)
    if plant_id:
        query += " AND plant_id=?"; params.append(plant_id)
    query += " ORDER BY created_at DESC"
    with connection() as db:
        rows = [dict(row) for row in db.execute(query, params)]
    for row in rows:
        row["top_predictions"] = decode_json(row["top_predictions"])
    return rows


@app.get("/api/v1/diagnoses/{diagnosis_id}")
def diagnosis_detail(diagnosis_id: str, user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    with connection() as db:
        row = owned(db, "diagnoses", diagnosis_id, user["id"])
    row["top_predictions"] = decode_json(row["top_predictions"])
    return row


@app.get("/api/v1/diagnoses/{diagnosis_id}/image")
def diagnosis_image(diagnosis_id: str, user: dict[str, Any] = Depends(current_user)) -> Response:
    with connection() as db:
        owned(db, "diagnoses", diagnosis_id, user["id"])
        image = row_dict(db.execute(
            "SELECT storage_key FROM diagnosis_images WHERE diagnosis_id=? AND user_id=?",
            (diagnosis_id, user["id"]),
        ).fetchone())
    if not image:
        raise HTTPException(404, "Diagnosis image not found")
    key = image["storage_key"]
    local_path = local_image_path(key)
    if local_path:
        return FileResponse(local_path)
    signed = presigned_image_url(key)
    if signed:
        return RedirectResponse(signed)
    raise HTTPException(404, "Private image storage is unavailable")


@app.delete("/api/v1/diagnoses/{diagnosis_id}")
def delete_diagnosis(diagnosis_id: str, user: dict[str, Any] = Depends(current_user)) -> dict[str, str]:
    with connection() as db:
        owned(db, "diagnoses", diagnosis_id, user["id"])
        image_rows = [dict(row) for row in db.execute("SELECT storage_key FROM diagnosis_images WHERE diagnosis_id=? AND user_id=?", (diagnosis_id, user["id"]))]
        db.execute("DELETE FROM scan_predictions WHERE diagnosis_id=?", (diagnosis_id,))
        db.execute("DELETE FROM diagnosis_images WHERE diagnosis_id=? AND user_id=?", (diagnosis_id, user["id"]))
        db.execute("DELETE FROM diagnoses WHERE id=?", (diagnosis_id,))
    for row in image_rows:
        delete_private_image(row["storage_key"])
    return {"message": "Diagnosis deleted"}


@app.post("/api/v1/diagnoses/{diagnosis_id}/feedback", status_code=201)
def add_feedback(diagnosis_id: str, payload: FeedbackRequest, user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    with connection() as db:
        owned(db, "diagnoses", diagnosis_id, user["id"])
        item_id = str(uuid.uuid4())
        db.execute("INSERT INTO feedback VALUES (?,?,?,?,?,?)", (item_id, user["id"], diagnosis_id, payload.rating, payload.comment, now()))
    return {"id": item_id, **payload.model_dump()}


@app.get("/api/v1/diagnoses/{diagnosis_id}/explanation")
def diagnosis_explanation(diagnosis_id: str, user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    with connection() as db:
        row = owned(db, "diagnoses", diagnosis_id, user["id"])
    if row["status"] == "unsupported_crop":
        return {
            "available": False,
            "method": "not_available",
            "message": "Không tạo bản đồ giải thích cho loại cây chưa nằm trong phạm vi.",
        }
    heatmap_path = row.get("explanation_path")
    return {
        "available": bool(heatmap_path),
        "method": "input-gradient",
        "message": "Grad-CAM tương đương: bản đồ input-gradient chỉ mô tả vùng ảnh ảnh hưởng dự đoán.",
    }


@app.get("/api/v1/diseases")
def diseases(search: str | None = None, plant: str | None = None, _: dict[str, Any] | None = Depends(lambda: None)) -> list[dict[str, Any]]:
    with connection() as db:
        rows = [dict(r) for r in db.execute("SELECT * FROM diseases ORDER BY name")]
    if search:
        rows = [r for r in rows if search.lower() in (r["name"] + r["name_vi"] + r["code"]).lower()]
    if plant:
        aliases = {
            "pepper": {"pepper", "pepper, bell", "bell pepper"},
            "corn": {"corn", "corn (maize)"},
            "orange": {"orange"},
        }
        wanted = aliases.get(plant.lower(), {plant.lower()})
        rows = [
            r for r in rows
            if r["plant"].lower() in wanted
            or plant.lower() in r["plant"].lower()
        ]
    return rows


@app.get("/api/v1/diseases/search")
def disease_search(q: str = Query(min_length=1)) -> list[dict[str, Any]]:
    return diseases(search=q)


@app.get("/api/v1/diseases/by-plant/{plant_id}")
def diseases_by_plant(plant_id: str) -> list[dict[str, Any]]:
    return diseases(plant=plant_id)


@app.get("/api/v1/diseases/{disease_id}")
def disease_detail(disease_id: str) -> dict[str, Any]:
    with connection() as db:
        row = row_dict(db.execute("SELECT * FROM diseases WHERE id=? OR code=?", (disease_id, disease_id)).fetchone())
    if not row:
        raise HTTPException(404, "Disease not found")
    return row


def analytics_for(user_id: str) -> dict[str, Any]:
    with connection() as db:
        count_row = db.execute("SELECT COUNT(*) AS count FROM plants WHERE user_id=?", (user_id,)).fetchone()
        total_plants = count_row["count"]
        rows = [dict(r) for r in db.execute("SELECT * FROM diagnoses WHERE user_id=? ORDER BY created_at DESC", (user_id,))]
    healthy = sum(r["status"] == "healthy" for r in rows)
    return {"total_plants": total_plants, "total_predictions": len(rows), "healthy_plants": healthy, "diseased_plants": len(rows) - healthy, "recent_diagnoses": rows[:10], "class_distribution": {k: sum(x["disease_code"] == k for x in rows) for k in sorted({x["disease_code"] for x in rows})}}


@app.get("/api/v1/analytics")
def analytics_legacy() -> dict[str, Any]:
    return diagnosis_service.analytics()


@app.get("/api/v1/analytics/dashboard")
def dashboard(user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    return analytics_for(user["id"])


@app.get("/api/v1/analytics/plant/{plant_id}")
def plant_analytics(plant_id: str, user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    with connection() as db:
        owned(db, "plants", plant_id, user["id"])
    rows = [r for r in list_diagnoses(user=user) if r["plant_id"] == plant_id]
    return {"plant_id": plant_id, "scans": rows, "trend": [{"date": r["created_at"], "confidence": r["confidence"], "severity": r["severity"]} for r in rows]}


@app.get("/api/v1/analytics/history/{plant_id}")
def history(plant_id: str, user: dict[str, Any] = Depends(current_user)) -> list[dict[str, Any]]:
    return plant_analytics(plant_id, user)["trend"]


@app.get("/api/v1/analytics/disease-distribution")
def disease_distribution(user: dict[str, Any] = Depends(current_user)) -> dict[str, int]:
    return analytics_for(user["id"])["class_distribution"]


@app.post("/api/v1/care-logs", status_code=201)
def create_care(payload: CareRequest, user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    item_id = str(uuid.uuid4())
    with connection() as db:
        if payload.plant_id: owned(db, "plants", payload.plant_id, user["id"])
        db.execute("INSERT INTO care_logs VALUES (?,?,?,?,?,?)", (item_id, user["id"], payload.plant_id, payload.kind, payload.note, payload.occurred_at or now(), now()))
    return {"id": item_id, **payload.model_dump(), "occurred_at": payload.occurred_at or now()}


@app.get("/api/v1/care-logs")
def list_care(user: dict[str, Any] = Depends(current_user)) -> list[dict[str, Any]]:
    with connection() as db:
        return [dict(r) for r in db.execute("SELECT * FROM care_logs WHERE user_id=? ORDER BY occurred_at DESC", (user["id"],))]


@app.put("/api/v1/care-logs/{care_id}")
def update_care(care_id: str, payload: CareRequest, user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    with connection() as db:
        row = row_dict(db.execute("SELECT id FROM care_logs WHERE id=? AND user_id=?", (care_id, user["id"])).fetchone())
        if not row:
            raise HTTPException(404, "Care log not found")
        if payload.plant_id:
            owned(db, "plants", payload.plant_id, user["id"])
        db.execute(
            "UPDATE care_logs SET plant_id=?,kind=?,note=?,occurred_at=? WHERE id=?",
            (payload.plant_id, payload.kind, payload.note, payload.occurred_at or now(), care_id),
        )
        return row_dict(db.execute("SELECT * FROM care_logs WHERE id=?", (care_id,)).fetchone())


@app.delete("/api/v1/care-logs/{care_id}")
def delete_care(care_id: str, user: dict[str, Any] = Depends(current_user)) -> dict[str, str]:
    with connection() as db:
        row = row_dict(db.execute("SELECT id FROM care_logs WHERE id=? AND user_id=?", (care_id, user["id"])).fetchone())
        if not row:
            raise HTTPException(404, "Care log not found")
        db.execute("DELETE FROM care_logs WHERE id=?", (care_id,))
    return {"message": "Care log deleted"}


@app.post("/api/v1/reminders", status_code=201)
def create_reminder(payload: ReminderRequest, user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    item_id = str(uuid.uuid4())
    with connection() as db:
        if payload.plant_id: owned(db, "plants", payload.plant_id, user["id"])
        db.execute("INSERT INTO reminders VALUES (?,?,?,?,?,?,?,?)", (item_id, user["id"], payload.plant_id, payload.kind, payload.due_at, payload.note, False, now()))
    return {"id": item_id, **payload.model_dump(), "completed": False}


@app.get("/api/v1/reminders")
def list_reminders(user: dict[str, Any] = Depends(current_user)) -> list[dict[str, Any]]:
    with connection() as db:
        return [dict(r) for r in db.execute("SELECT * FROM reminders WHERE user_id=? ORDER BY due_at", (user["id"],))]


@app.put("/api/v1/reminders/{reminder_id}")
def update_reminder(reminder_id: str, payload: ReminderRequest, user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    with connection() as db:
        owned(db, "reminders", reminder_id, user["id"])
        if payload.plant_id:
            owned(db, "plants", payload.plant_id, user["id"])
        db.execute(
            "UPDATE reminders SET plant_id=?,kind=?,due_at=?,note=? WHERE id=?",
            (payload.plant_id, payload.kind, payload.due_at, payload.note, reminder_id),
        )
        return row_dict(db.execute("SELECT * FROM reminders WHERE id=?", (reminder_id,)).fetchone())


@app.post("/api/v1/reminders/{reminder_id}/complete")
def complete_reminder(reminder_id: str, payload: ReminderCompleteRequest, user: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    with connection() as db:
        owned(db, "reminders", reminder_id, user["id"])
        db.execute("UPDATE reminders SET completed=? WHERE id=?", (payload.completed, reminder_id))
        return row_dict(db.execute("SELECT * FROM reminders WHERE id=?", (reminder_id,)).fetchone())


@app.delete("/api/v1/reminders/{reminder_id}")
def delete_reminder(reminder_id: str, user: dict[str, Any] = Depends(current_user)) -> dict[str, str]:
    with connection() as db:
        row = owned(db, "reminders", reminder_id, user["id"])
        db.execute("DELETE FROM reminders WHERE id=?", (row["id"],))
    return {"message": "Reminder deleted"}


@app.get("/api/v1/notifications")
def list_notifications(user: dict[str, Any] = Depends(current_user)) -> list[dict[str, Any]]:
    with connection() as db:
        return [dict(r) for r in db.execute("SELECT * FROM notifications WHERE user_id=? ORDER BY created_at DESC", (user["id"],))]


@app.post("/api/v1/notifications/{notification_id}/read")
def read_notification(notification_id: str, user: dict[str, Any] = Depends(current_user)) -> dict[str, str]:
    with connection() as db:
        row = row_dict(db.execute("SELECT id FROM notifications WHERE id=? AND user_id=?", (notification_id, user["id"])).fetchone())
        if not row:
            raise HTTPException(404, "Notification not found")
        db.execute("UPDATE notifications SET is_read=? WHERE id=?", (True, notification_id))
    return {"message": "Notification marked as read"}


@app.get("/api/v1/reports/plant/{plant_id}.pdf")
def plant_report(plant_id: str, user: dict[str, Any] = Depends(current_user)) -> Response:
    plant = get_plant(plant_id, user)
    rows = plant_analytics(plant_id, user)["scans"]
    with connection() as db:
        care_rows = [dict(row) for row in db.execute(
            "SELECT kind,note,occurred_at FROM care_logs WHERE user_id=? AND plant_id=? ORDER BY occurred_at DESC",
            (user["id"], plant_id),
        )]
    lines = [
        "SMART PLANT CARE AI - PLANT HEALTH REPORT",
        f"Plant: {plant['name']} ({plant['species']})",
        f"Location: {plant.get('location') or 'Not provided'}",
        f"Monitoring since: {plant.get('started_at') or 'Not provided'}",
        f"Generated: {now()}",
        "",
        f"Total AI checks: {len(rows)}",
        f"Healthy checks: {sum(row['status'] == 'healthy' for row in rows)}",
        f"Checks needing review: {sum(row['status'] in {'uncertain', 'unsupported_crop'} for row in rows)}",
        f"Care activities recorded: {len(care_rows)}",
        "",
        "DIAGNOSIS HISTORY",
    ]
    for row in rows:
        lines.append(f"{row.get('created_at', '')} | {row.get('disease_code', '')} | {row.get('status', '')} | confidence {float(row.get('confidence') or 0):.1%}")
    lines.extend(["", "CARE JOURNAL"])
    for row in care_rows:
        lines.append(f"{row.get('occurred_at', '')} | {row.get('kind', '')} | {row.get('note') or ''}")
    lines.extend(["", "Note: Image classification does not measure whole-plant health or clinical disease severity."])
    content = make_pdf(lines)
    return Response(content, media_type="application/pdf", headers={"Content-Disposition": f'attachment; filename="plant-report-{plant_id}.pdf"'})


def make_pdf(lines: list[str]) -> bytes:
    """Build a small, standards-compliant multi-page PDF using built-in Helvetica."""
    normalized = [unicodedata.normalize("NFKD", line).encode("ascii", "ignore").decode("ascii") for line in lines]
    wrapped: list[str] = []
    for line in normalized:
        while len(line) > 92:
            wrapped.append(line[:92])
            line = "  " + line[92:]
        wrapped.append(line)
    page_lines = [wrapped[index:index + 45] for index in range(0, max(1, len(wrapped)), 45)]
    objects: list[bytes] = [b""]
    page_ids = [3 + index * 2 for index in range(len(page_lines))]
    font_id = 3 + len(page_lines) * 2
    objects.append(f"<< /Type /Catalog /Pages 2 0 R >>".encode())
    objects.append(f"<< /Type /Pages /Kids [{' '.join(f'{page_id} 0 R' for page_id in page_ids)}] /Count {len(page_ids)} >>".encode())
    for page_id, content_id, text_lines in zip(page_ids, (page_id + 1 for page_id in page_ids), page_lines):
        commands = ["BT", "/F1 10 Tf", "48 790 Td", "14 TL"]
        for index, line in enumerate(text_lines):
            escaped = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            commands.append(f"({escaped}) Tj")
            if index < len(text_lines) - 1:
                commands.append("T*")
        commands.append("ET")
        stream = "\n".join(commands).encode("latin-1")
        objects.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 842] /Resources << /Font << /F1 {font_id} 0 R >> >> /Contents {content_id} 0 R >>".encode())
        objects.append(b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream")
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for object_id, body in enumerate(objects[1:], start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{object_id} 0 obj\n".encode() + body + b"\nendobj\n")
    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(objects)}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode())
    pdf.extend(f"trailer\n<< /Size {len(objects)} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode())
    return bytes(pdf)


@app.get("/api/v1/admin/users")
def admin_users(_: dict[str, Any] = Depends(admin_user)) -> list[dict[str, Any]]:
    with connection() as db:
        return [dict(r) for r in db.execute("SELECT id,email,name,role,is_active,created_at FROM users ORDER BY created_at DESC")]


@app.post("/api/v1/admin/users/{user_id}/lock")
def admin_lock_user(user_id: str, _: dict[str, Any] = Depends(admin_user)) -> dict[str, Any]:
    with connection() as db:
        row = row_dict(db.execute("SELECT id,email,name,role,is_active,created_at FROM users WHERE id=?", (user_id,)).fetchone())
        if not row:
            raise HTTPException(404, "User not found")
        db.execute("UPDATE users SET is_active=? WHERE id=?", (not bool(row["is_active"]), user_id))
        row["is_active"] = not bool(row["is_active"])
    return row


@app.get("/api/v1/admin/audit-logs")
def admin_audit_logs(_: dict[str, Any] = Depends(admin_user)) -> list[dict[str, Any]]:
    with connection() as db:
        return [dict(r) for r in db.execute("SELECT * FROM audit_logs ORDER BY created_at DESC")]


@app.get("/api/v1/admin/scans")
def admin_scans(_: dict[str, Any] = Depends(admin_user)) -> list[dict[str, Any]]:
    with connection() as db:
        return [dict(r) for r in db.execute("SELECT * FROM diagnoses ORDER BY created_at DESC")]


@app.post("/api/v1/admin/diseases", status_code=201)
def admin_create_disease(payload: DiseaseRequest, _: dict[str, Any] = Depends(admin_user)) -> dict[str, Any]:
    item_id = str(uuid.uuid4())
    with connection() as db:
        db.execute("INSERT INTO diseases VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (item_id, payload.code, payload.plant, payload.name, payload.name_vi, payload.pathogen, payload.symptoms, payload.conditions, payload.treatment, payload.prevention, payload.image_url, now()))
    return {"id": item_id, **payload.model_dump()}


@app.put("/api/v1/admin/diseases/{disease_id}")
def admin_update_disease(disease_id: str, payload: DiseaseRequest, _: dict[str, Any] = Depends(admin_user)) -> dict[str, Any]:
    with connection() as db:
        if not db.execute("SELECT 1 FROM diseases WHERE id=?", (disease_id,)).fetchone(): raise HTTPException(404, "Disease not found")
        db.execute("UPDATE diseases SET code=?,plant=?,name=?,name_vi=?,pathogen=?,symptoms=?,conditions=?,treatment=?,prevention=?,image_url=? WHERE id=?", (*payload.model_dump().values(), disease_id))
    return disease_detail(disease_id)


@app.delete("/api/v1/admin/diseases/{disease_id}")
def admin_delete_disease(disease_id: str, _: dict[str, Any] = Depends(admin_user)) -> dict[str, str]:
    with connection() as db:
        if not db.execute("SELECT 1 FROM diseases WHERE id=?", (disease_id,)).fetchone():
            raise HTTPException(404, "Disease not found")
        db.execute("DELETE FROM diseases WHERE id=?", (disease_id,))
    return {"message": "Disease deleted"}


@app.get("/api/v1/admin/plants")
def admin_plants(_: dict[str, Any] = Depends(admin_user)) -> list[dict[str, Any]]:
    with connection() as db:
        return [dict(r) for r in db.execute("SELECT * FROM plants ORDER BY created_at DESC")]


@app.get("/api/v1/admin/models")
def admin_models(_: dict[str, Any] = Depends(admin_user)) -> list[dict[str, Any]]:
    with connection() as db:
        return [dict(r) for r in db.execute("SELECT * FROM model_versions ORDER BY created_at DESC")]


@app.post("/api/v1/admin/models", status_code=201)
def admin_create_model(payload: ModelRequest, _: dict[str, Any] = Depends(admin_user)) -> dict[str, Any]:
    item_id = str(uuid.uuid4())
    with connection() as db:
        db.execute(
            "INSERT INTO model_versions "
            "(id,name,version,status,metrics,created_at,architecture,dataset_version,class_count,weights_path,preprocessing_config,threshold_config) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                item_id, payload.name, payload.version, payload.status,
                __import__("json").dumps(payload.metrics), now(), payload.architecture,
                payload.dataset_version, payload.class_count, payload.weights_path,
                __import__("json").dumps(payload.preprocessing_config),
                __import__("json").dumps(payload.threshold_config),
            ),
        )
    return {"id": item_id, **payload.model_dump()}


@app.get("/api/v1/admin/model-evaluations")
def admin_evaluations(_: dict[str, Any] = Depends(admin_user)) -> dict[str, Any]:
    report_path = __import__("pathlib").Path(__file__).parents[1] / "models" / "plant_health.evaluation.json"
    if not report_path.exists():
        raise HTTPException(503, "Model evaluation report is not available; run scripts/evaluate.py first")
    return {"metrics": ["accuracy", "top3_accuracy", "macro_precision", "macro_recall", "macro_f1"], "evaluation": __import__("json").loads(report_path.read_text())}


@app.post("/api/v1/qa")
def ask_question(request: QuestionRequest) -> dict[str, Any]:
    return qa_service.answer(request.question)
