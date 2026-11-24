from __future__ import annotations

import json
import os
import logging
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator
from urllib.parse import urlsplit

from app.config import APP_ENV

logger = logging.getLogger("smart-plant-care.storage")


DB_PATH = Path(os.getenv("DATABASE_PATH", Path(__file__).parents[1] / "data" / "smart_plant_care.db"))
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()


class PostgresWrapper:
    def __init__(self, connection: Any):
        self.connection = connection

    def execute(self, sql: str, params: Any = ()) -> "PostgresCursor":
        sql = sql.replace("?", "%s")
        sql = sql.replace("datetime('now')", "CURRENT_TIMESTAMP")
        if "INSERT OR IGNORE INTO" in sql:
            sql = sql.replace("INSERT OR IGNORE INTO", "INSERT INTO")
            sql = sql.rstrip().rstrip(";") + " ON CONFLICT DO NOTHING"
        sql = sql.replace("PRAGMA table_info(model_versions)", "SELECT 1")
        cursor = self.connection.cursor()
        cursor.execute(sql, params)
        return PostgresCursor(cursor)

    def executemany(self, sql: str, params: Any) -> "PostgresCursor":
        sql = sql.replace("?", "%s")
        cursor = self.connection.cursor()
        cursor.executemany(sql, params)
        return PostgresCursor(cursor)

    def executescript(self, sql: str) -> None:
        sql = sql.replace("?", "%s").replace("INTEGER NOT NULL DEFAULT", "INTEGER NOT NULL DEFAULT")
        sql = sql.replace("TEXT PRIMARY KEY", "TEXT PRIMARY KEY")
        sql = sql.replace("datetime('now')", "CURRENT_TIMESTAMP")
        with self.connection.cursor() as cursor:
            for statement in sql.split(";"):
                statement = statement.strip()
                if statement:
                    if "INSERT OR IGNORE INTO" in statement:
                        statement = statement.replace("INSERT OR IGNORE INTO", "INSERT INTO")
                        statement += " ON CONFLICT DO NOTHING"
                    cursor.execute(statement)

    def commit(self) -> None:
        self.connection.commit()

    def rollback(self) -> None:
        self.connection.rollback()

    def close(self) -> None:
        self.connection.close()


class PostgresCursor:
    def __init__(self, cursor: Any):
        self.cursor = cursor

    def fetchone(self) -> dict[str, Any] | None:
        if not getattr(self.cursor, "description", None):
            return None
        columns = [column.name for column in self.cursor.description]
        row = self.cursor.fetchone()
        return dict(zip(columns, row)) if row else None

    def fetchall(self) -> list[Any]:
        if not getattr(self.cursor, "description", None):
            return []
        columns = [column.name for column in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

    def __iter__(self) -> Iterator[Any]:
        columns = [column.name for column in self.cursor.description]
        for row in self.cursor.fetchall():
            yield dict(zip(columns, row))


@contextmanager
def connection() -> Iterator[Any]:
    started = time.perf_counter()
    if DATABASE_URL:
        if not DATABASE_URL.startswith(("postgresql://", "postgres://")):
            raise RuntimeError("DATABASE_URL must be the PostgreSQL connection string from Supabase Dashboard > Connect")
        db_host = urlsplit(DATABASE_URL).hostname or "unknown"
        logger.info("postgres_connection_started provider=supabase host=%s", db_host)
        try:
            import psycopg
            raw = psycopg.connect(DATABASE_URL, connect_timeout=10, sslmode="require")
            db: Any = PostgresWrapper(raw)
            logger.debug("postgres_connection_opened provider=supabase")
        except Exception as exc:
            message = str(exc).lower()
            if "getaddrinfo failed" in message or "name or service not known" in message or "temporary failure in name resolution" in message:
                logger.exception("postgres_connection_failed provider=supabase cause=dns_resolution host=%s", db_host)
                raise RuntimeError(
                    "Supabase database hostname cannot be resolved from this network. In Supabase Dashboard > Connect, "
                    "copy the Session pooler connection string (or Transaction pooler if that is the available IPv4 option), "
                    "then set DATABASE_URL to that exact URI and restart. Direct db.<project>.supabase.co may be IPv6-only."
                ) from exc
            logger.exception("postgres_connection_failed provider=supabase host=%s", db_host)
            raise RuntimeError("Supabase PostgreSQL connection failed; verify the Dashboard > Connect URI, password, network, and SSL") from exc
    elif APP_ENV == "test":
        import sqlite3

        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        db = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    else:
        raise RuntimeError("DATABASE_URL is required; local SQLite is disabled for application data")
    try:
        yield db
        db.commit()
        logger.debug("database_transaction_committed backend=%s duration_ms=%.2f", "supabase_postgres" if DATABASE_URL else "test_sqlite", (time.perf_counter() - started) * 1000)
    except Exception:
        try:
            db.rollback()
        except Exception:
            logger.exception("database_rollback_failed backend=%s", "supabase_postgres" if DATABASE_URL else "test_sqlite")
        logger.exception("database_transaction_failed backend=%s duration_ms=%.2f", "supabase_postgres" if DATABASE_URL else "test_sqlite", (time.perf_counter() - started) * 1000)
        raise
    finally:
        db.close()


def init_db() -> None:
    if not DATABASE_URL and APP_ENV != "test":
        raise RuntimeError("DATABASE_URL is required; copy the PostgreSQL connection string from Supabase Dashboard > Connect")
    if DATABASE_URL and not DATABASE_URL.startswith(("postgresql://", "postgres://")):
        raise RuntimeError("DATABASE_URL is an HTTPS API URL; use the PostgreSQL connection string from Supabase Dashboard > Connect")
    logger.info("database_initialization_started backend=%s", "supabase_postgres" if DATABASE_URL else "test_sqlite")
    with connection() as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY, email TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL,
                name TEXT NOT NULL, role TEXT NOT NULL DEFAULT 'USER', is_active BOOLEAN NOT NULL DEFAULT TRUE,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS plants (
                id TEXT PRIMARY KEY, user_id TEXT NOT NULL, name TEXT NOT NULL, species TEXT NOT NULL,
                variety TEXT, started_at TEXT, location TEXT, notes TEXT, image_path TEXT,
                status TEXT NOT NULL DEFAULT 'active', created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS diseases (
                id TEXT PRIMARY KEY, code TEXT UNIQUE NOT NULL, plant TEXT NOT NULL, name TEXT NOT NULL,
                name_vi TEXT NOT NULL, pathogen TEXT, symptoms TEXT NOT NULL, conditions TEXT NOT NULL,
                treatment TEXT NOT NULL, prevention TEXT NOT NULL, image_url TEXT, created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS diagnoses (
                id TEXT PRIMARY KEY, user_id TEXT NOT NULL, plant_id TEXT, filename TEXT,
                image_path TEXT, plant TEXT NOT NULL, disease_code TEXT NOT NULL, status TEXT NOT NULL,
                confidence REAL NOT NULL, top_predictions TEXT NOT NULL, recommendation TEXT NOT NULL,
                model_version TEXT NOT NULL, severity TEXT NOT NULL, note TEXT, created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS care_logs (
                id TEXT PRIMARY KEY, user_id TEXT NOT NULL, plant_id TEXT, kind TEXT NOT NULL,
                note TEXT, occurred_at TEXT NOT NULL, created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS reminders (
                id TEXT PRIMARY KEY, user_id TEXT NOT NULL, plant_id TEXT, kind TEXT NOT NULL,
                due_at TEXT NOT NULL, note TEXT, completed BOOLEAN NOT NULL DEFAULT FALSE, created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS feedback (
                id TEXT PRIMARY KEY, user_id TEXT NOT NULL, diagnosis_id TEXT NOT NULL,
                rating INTEGER, comment TEXT, created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS diagnosis_images (
                id TEXT PRIMARY KEY, diagnosis_id TEXT NOT NULL, user_id TEXT NOT NULL,
                storage_key TEXT NOT NULL, filename TEXT, created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS scan_predictions (
                id TEXT PRIMARY KEY, diagnosis_id TEXT NOT NULL, class_code TEXT NOT NULL,
                class_name TEXT NOT NULL, confidence REAL NOT NULL, rank INTEGER NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS model_versions (
                id TEXT PRIMARY KEY, name TEXT NOT NULL, version TEXT UNIQUE NOT NULL,
                status TEXT NOT NULL, metrics TEXT NOT NULL, created_at TEXT NOT NULL,
                architecture TEXT, dataset_version TEXT, class_count INTEGER,
                weights_path TEXT, preprocessing_config TEXT, threshold_config TEXT
            );
            CREATE TABLE IF NOT EXISTS roles (
                id TEXT PRIMARY KEY, name TEXT UNIQUE NOT NULL
            );
            CREATE TABLE IF NOT EXISTS notifications (
                id TEXT PRIMARY KEY, user_id TEXT NOT NULL, title TEXT NOT NULL,
                message TEXT NOT NULL, kind TEXT NOT NULL, is_read BOOLEAN NOT NULL DEFAULT FALSE,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS audit_logs (
                id TEXT PRIMARY KEY, actor_id TEXT NOT NULL, action TEXT NOT NULL,
                target_type TEXT NOT NULL, target_id TEXT, details TEXT, created_at TEXT NOT NULL
            );
            INSERT OR IGNORE INTO roles (id,name) VALUES ('role-user','USER'),('role-admin','ADMIN');
            """
        )
        if APP_ENV == "test":
            existing = {row["name"] for row in db.execute("PRAGMA table_info(model_versions)")}
            model_columns = {
                "architecture": "TEXT",
                "dataset_version": "TEXT",
                "class_count": "INTEGER",
                "weights_path": "TEXT",
                "preprocessing_config": "TEXT",
                "threshold_config": "TEXT",
            }
            for column, column_type in model_columns.items():
                if column not in existing:
                    db.execute(f"ALTER TABLE model_versions ADD COLUMN {column} {column_type}")
        for disease in DEFAULT_DISEASES:
            db.execute(
                """INSERT OR IGNORE INTO diseases
                (id,code,plant,name,name_vi,pathogen,symptoms,conditions,treatment,prevention,created_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,datetime('now'))""",
                disease,
            )
        admin_email = os.getenv("ADMIN_EMAIL")
        admin_password = os.getenv("ADMIN_PASSWORD")
        if admin_email and admin_password:
            from app.security import hash_password

            db.execute(
                """INSERT OR IGNORE INTO users
                (id,email,password_hash,name,role,is_active,created_at)
                VALUES (?,?,?,?,?,?,?)""",
                ("admin", admin_email.lower(), hash_password(admin_password), "Administrator", "ADMIN", True, now_iso()),
            )
    logger.info("database_initialization_succeeded backend=%s", "supabase_postgres" if DATABASE_URL else "test_sqlite")


def now_iso() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat()


DEFAULT_DISEASES = [
    ("disease-orange-hlb", "orange_hlb", "Orange", "Citrus Greening", "Bệnh vàng lá gân xanh", "Candidatus Liberibacter asiaticus", "Lá vàng loang lổ, gân lá xanh; quả nhỏ, méo hoặc chín không đều.", "Lây truyền chủ yếu qua rầy chổng cánh; cây giống nhiễm bệnh làm bệnh lan xa.", "Cách ly và báo cơ quan bảo vệ thực vật địa phương để được hướng dẫn xử lý cây bệnh.", "Dùng cây giống sạch bệnh và quản lý rầy chổng cánh theo khuyến cáo địa phương."),
    ("disease-apple-scab","apple_scab","Apple","Apple Scab","Bệnh ghẻ táo","Venturia inaequalis","Đốm oliu nâu trên lá","Lá ướt kéo dài và thông thoáng kém","Thu gom lá rụng, tỉa cành và tránh tưới lên lá.","Giữ tán lá thông thoáng và vệ sinh lá rụng."),
    ("disease-apple-black-rot","apple_black_rot","Apple","Apple Black Rot","Bệnh thối đen táo","Botryosphaeria obtusa","Vết nâu sẫm, lan từ lá sang quả","Độ ẩm cao và vết thương trên lá","Loại bỏ lá/cành bệnh, vệ sinh dụng cụ.","Cắt tỉa cành xấu và luân chuyển tưới."),
    ("disease-apple-rust","apple_cedar_rust","Apple","Cedar Apple Rust","Bệnh gỉ táo","Gymnosporangium juniperi-virginianae","Đốm cam/vàng trên lá","Lá ướt kéo dài gần cây host","Loại bỏ lá nặng bệnh và hạn chế lá ướt lâu.","Tưới gốc và tăng khoảng cách thông thoáng."),
    ("disease-apple-healthy","apple_healthy","Apple","Healthy","Táo khỏe mạnh","Không phát hiện tác nhân","Không phát hiện tổn thương lá rõ ràng","Điều kiện chăm sóc bình thường","Tiếp tục theo dõi theo lịch.","Duy trì tưới đúng, dinh dưỡng cân bằng và vệ sinh lá rụng."),
    ("disease-blueberry-healthy","blueberry_healthy","Blueberry","Healthy","Việt quất khỏe mạnh","Không phát hiện tác nhân","Không phát hiện tổn thương lá rõ ràng","Điều kiện chăm sóc bình thường","Tiếp tục theo dõi lá mới.","Giữ đất thoát nước tốt và tưới đều."),
    ("disease-cherry-powdery-mildew","cherry_powdery_mildew","Cherry","Powdery Mildew","Bệnh phấn trắng anh đào","Erysiphaceae","Bột trắng trên mặt lá","Ẩm, thông thoáng kém","Loại bỏ lá nặng, tăng thông thoáng.","Tránh tưới lên lá và vệ sinh lá rụng."),
    ("disease-cherry-healthy","cherry_healthy","Cherry","Healthy","Anh đào khỏe mạnh","Không phát hiện tác nhân","Không phát hiện tổn thương lá rõ ràng","Điều kiện chăm sóc bình thường","Tiếp tục theo dõi.","Duy trì tưới gốc và thông thoáng."),
    ("disease-corn-gray-leaf","corn_gray_leaf_spot","Corn","Gray Leaf Spot","Bệnh đốm lá xám ngô","Cercospora zeae-maydis","Vết chữ nhật xám nâu dọc gân lá","Nhiệt ẩm cao kéo dài","Loại bỏ tàn dư lá nặng và theo dõi.","Luân canh và chọn giống phù hợp."),
    ("disease-corn-rust","corn_common_rust","Corn","Common Rust","Gỉ sắt ngô","Puccinia sorghi","Bào tử nâu cam trên lá","Lá ẩm và thời tiết thích hợp nấm","Loại lá nặng và theo dõi lan rộng.","Tưới gốc, luân canh."),
    ("disease-corn-northern-leaf","corn_northern_leaf_blight","Corn","Northern Leaf Blight","Bệnh cháy lá lớn ngô","Exserohilum turcicum","Vệt nâu dài, kiểu chữ sáo","Nhiệt độ ấm và lá ướt lâu","Giữ tàn dư sạch, kiểm tra lá.","Luân canh và thông thoáng."),
    ("disease-corn-healthy","corn_healthy","Corn","Healthy","Ngô khỏe mạnh","Không phát hiện tác nhân","Không phát hiện tổn thương lá rõ ràng","Điều kiện chăm sóc bình thường","Theo dõi lại khi lá có dấu hiệu mới.","Duy trì dinh dưỡng và tưới đều."),
    ("disease-grape-black-rot","grape_black_rot","Grape","Black Rot","Thối đen nho","Guignardia bidwellii","Vết nâu, sau đen và khô","Ẩm cao và lá ướt lâu","Loại lá/quả bệnh, vệ sinh tàn dư.","Tăng thông thoáng và tưới gốc."),
    ("disease-grape-esca","grape_esca","Grape","Esca/Black Measles","Bệnh Esca nho","Phức hợp nấm mộc","Vệt đỏ/nâu và sọc đen","Cây già, vết cắt và nấm mộc","Cắt phần cây nặng và vệ sinh dụng cụ.","Tránh tạo vết thương; kiểm tra cành."),
    ("disease-grape-leaf-blight","grape_leaf_blight","Grape","Leaf Blight","Cháy lá nho","Pseudocercospora vitis","Vết nâu lan trên lá","Ẩm độ cao","Loại lá nặng và giữ tán lá thoáng.","Không tưới lên lá."),
    ("disease-grape-healthy","grape_healthy","Grape","Healthy","Nho khỏe mạnh","Không phát hiện tác nhân","Không phát hiện tổn thương lá rõ ràng","Điều kiện chăm sóc bình thường","Tiếp tục theo dõi.","Duy trì tưới gốc và tỉa cành."),
    ("disease-orange-citrus-greening","orange_citrus_greening","Orange","Citrus Greening","Xanh hóa cam/quýt","Candidatus Liberibacter","Vàng lá không đối xứng, chồi còi","Dưới ấm sâu hút mầm","Cách ly cây nghi bệnh và liên hệ chuyên gia.","Kiểm soát sâu/tuyến trùng truyền bệnh."),
    ("disease-peach-bacterial-spot","peach_bacterial_spot","Peach","Bacterial Spot","Đốm vi khuẩn đào","Xanthomonas arboricola pv. pruni","Đốm nâu/hở rìa lá","Mưa và gió làm lá thương","Loại lá nặng và tránh tưới lên lá.","Giữ vùng trồng thoáng."),
    ("disease-peach-healthy","peach_healthy","Peach","Healthy","Đào khỏe mạnh","Không phát hiện tác nhân","Không phát hiện tổn thương lá rõ ràng","Điều kiện chăm sóc bình thường","Tiếp tục theo dõi.","Tưới gốc và giữ vườn sạch."),
    ("disease-pepper-bacterial-spot","pepper_bacterial_spot","Pepper, bell","Bacterial Spot","Đốm vi khuẩn ớt chuông","Xanthomonas spp.","Vết nâu, lá vàng và rụng","Ấm ẩm, lá ướt","Cách ly lá bệnh và tham khảo biện pháp địa phương.","Không tưới lá ướt và vệ sinh dụng cụ."),
    ("disease-pepper-healthy","pepper_healthy","Pepper, bell","Healthy","Ớt chuông khỏe mạnh","Không phát hiện tác nhân","Không phát hiện tổn thương lá rõ ràng","Điều kiện chăm sóc bình thường","Tiếp tục theo dõi.","Tưới gốc và thông thoáng."),
    ("disease-potato-early-blight","potato_early_blight","Potato","Early Blight","Đốm vòng sớm khoai tây","Alternaria solani","Đốm nâu có vòng đồng tâm","Lá già và lá ướt kéo dài","Loại lá già nặng và giữ lá khô.","Luân canh, tưới gốc."),
    ("disease-potato-late-blight","potato_late_blight","Potato","Late Blight","Mốc sương khoai tây","Phytophthora infestans","Vết nâu lan nhanh","Mát ẩm và lá ướt lâu","Cách ly cây nặng, tham khảo chuyên gia.","Giảm ẩm lá và vệ sinh tàn dư."),
    ("disease-potato-healthy","potato_healthy","Potato","Healthy","Khoai tây khỏe mạnh","Không phát hiện tác nhân","Không phát hiện tổn thương lá rõ ràng","Điều kiện chăm sóc bình thường","Tiếp tục theo dõi.","Tưới đều và luân canh."),
    ("disease-raspberry-healthy","raspberry_healthy","Raspberry","Healthy","Mâm xôi khỏe mạnh","Không phát hiện tác nhân","Không phát hiện tổn thương lá rõ ràng","Điều kiện chăm sóc bình thường","Tiếp tục theo dõi.","Tưới gốc và tỉa cành."),
    ("disease-soybean-healthy","soybean_healthy","Soybean","Healthy","Đậu nành khỏe mạnh","Không phát hiện tác nhân","Không phát hiện tổn thương lá rõ ràng","Điều kiện chăm sóc bình thường","Tiếp tục theo dõi.","Duy trì dinh dưỡng và luân canh."),
    ("disease-squash-powdery-mildew","squash_powdery_mildew","Squash","Powdery Mildew","Phấn trắng bí","Podosphaera xanthii","Vùng trắng bột trên lá","Thông thoáng kém, lá ẩm","Loại lá nặng và tăng thông thoáng.","Không tưới lên lá."),
    ("disease-strawberry-leaf-scorch","strawberry_leaf_scorch","Strawberry","Leaf Scorch","Cháy lá dâu tây","Diplocarpon earlianum","Vết tím/nâu lan theo mép lá","Nhiệt và lá ướt kéo dài","Loại lá nặng và giữ lá khô.","Tưới gốc, vệ sinh lá rụng."),
    ("disease-strawberry-healthy","strawberry_healthy","Strawberry","Healthy","Dâu tây khỏe mạnh","Không phát hiện tác nhân","Không phát hiện tổn thương lá rõ ràng","Điều kiện chăm sóc bình thường","Tiếp tục theo dõi.","Tưới đều và giữ lá khô."),
    ("disease-tomato-bacterial","tomato_bacterial_spot","Tomato","Bacterial Spot","Đốm vi khuẩn cà chua","Xanthomonas spp.","Đốm nâu nhỏ, lá vàng/rụng","Ấm ẩm, lá ướt","Cách ly lá bệnh, không tưới lên lá.","Vệ sinh dụng cụ và luân canh."),
    ("disease-tomato-early","tomato_early_blight","Tomato","Early Blight","Đốm vòng sớm cà chua","Alternaria solani","Đốm nâu có vòng đồng tâm","Lá già ẩm kéo dài","Loại lá nặng, giữ lá khô.","Tưới gốc, vệ sinh lá rụng."),
    ("disease-tomato-late","tomato_late_blight","Tomato","Late Blight","Mốc sương cà chua","Phytophthora infestans","Vết nâu lan nhanh, có mốc","Mát ẩm và lá ướt lâu","Cách ly cây nặng, tham khảo chuyên gia.","Giảm lá ướt và luân canh."),
    ("disease-tomato-leaf-mold","tomato_leaf_mold","Tomato","Leaf Mold","Mốc lá cà chua","Passalora fulva","Mốc vàng/nâu dưới mặt lá","Nhà kính ẩm cao","Thông thoáng, loại lá nặng.","Giảm độ ẩm và tưới gốc."),
    ("disease-tomato-septoria","tomato_septoria_leaf_spot","Tomato","Septoria Leaf Spot","Đốm Septoria cà chua","Septoria lycopersici","Nhiều đốm tròn nhỏ có chấm đen","Lá ướt kéo dài","Loại lá nặng, giữ lá khô.","Vệ sinh lá rụng và tưới gốc."),
    ("disease-tomato-spider-mites","tomato_spider_mites","Tomato","Spider Mites","Nhện đỏ/two-spotted cà chua","Tetranychus urticae","Đốm vàng, mạng nhện dưới lá","Khô nóng và thiếu thông thoáng","Loại lá nặng và giám sát sâu hại.","Tăng độ ẩm vừa phải, kiểm tra sâu."),
    ("disease-tomato-target","tomato_target_spot","Tomato","Target Spot","Đốm mục tiêu cà chua","Corynespora cassiicola","Đốm nâu có vòng đồng tâm","Lá ướt, ấm ẩm","Loại lá nặng và giữ lá khô.","Tưới gốc và tăng thông thoáng."),
    ("disease-tomato-mosaic","tomato_mosaic_virus","Tomato","Tomato Mosaic Virus","Virus khảm cà chua","Tobamovirus","Mảng xanh-vàng, lá méo","Virus lây qua dụng cụ/cây giống","Cách ly cây nghi nhiễm.","Vệ sinh dụng cụ và dùng cây giống khỏe."),
    ("disease-tomato-yellow-curl","tomato_yellow_leaf_curl","Tomato","Tomato Yellow Leaf Curl","Virus xoăn vàng lá cà chua","Begomovirus","Lá vàng, cuộn, chồi còi","Bệnh nhân qua rầy trắng","Cách ly cây và kiểm soát rầy trắng.","Lưới chắn và quản lý côn trùng."),
    ("disease-tomato-healthy","tomato_healthy","Tomato","Healthy","Cà chua khỏe mạnh","Không phát hiện tác nhân","Không phát hiện tổn thương lá rõ ràng","Điều kiện chăm sóc bình thường","Tiếp tục theo dõi.","Tưới đều, thông thoáng và vệ sinh lá."),
]


def row_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    return dict(row) if row else None


def decode_json(value: str) -> Any:
    return json.loads(value)
