"""Keep automated tests isolated from Supabase and user upload storage."""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

os.environ["APP_ENV"] = "test"
os.environ["DATABASE_URL"] = ""
os.environ["STORAGE_BACKEND"] = "disabled"
os.environ["DATABASE_PATH"] = str(Path(tempfile.gettempdir()) / f"smart-plant-care-tests-{os.getpid()}.db")
os.environ["ADMIN_EMAIL"] = ""
os.environ["ADMIN_PASSWORD"] = ""
