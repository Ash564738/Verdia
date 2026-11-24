from __future__ import annotations

import argparse
import os
import sqlite3
from pathlib import Path

try:
    import psycopg
except ImportError as exc:
    raise SystemExit("Install psycopg[binary] before migration") from exc


TABLES = [
    "users",
    "plants",
    "diseases",
    "diagnoses",
    "diagnosis_images",
    "scan_predictions",
    "care_logs",
    "reminders",
    "notifications",
    "feedback",
    "model_versions",
    "model_evaluations",
    "audit_logs",
]


def copy_table(source: sqlite3.Connection, target: psycopg.Connection, table: str) -> int:
    try:
        rows = source.execute(f"SELECT * FROM {table}").fetchall()
        columns = [item[1] for item in source.execute(f"PRAGMA table_info({table})").fetchall()]
    except sqlite3.OperationalError:
        return 0
    if not rows:
        return 0
    placeholders = ", ".join(["%s"] * len(columns))
    column_sql = ", ".join(columns)
    with target.cursor() as cursor:
        cursor.executemany(
            f"INSERT INTO {table} ({column_sql}) VALUES ({placeholders}) "
            "ON CONFLICT DO NOTHING",
            [tuple(row) for row in rows],
        )
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sqlite", type=Path, default=Path("data/smart_plant_care.db"))
    parser.add_argument("--database-url", default=os.getenv("DATABASE_URL"))
    args = parser.parse_args()
    if not args.database_url:
        raise SystemExit("Set DATABASE_URL or pass --database-url")
    if not args.sqlite.exists():
        raise SystemExit(f"SQLite database not found: {args.sqlite}")

    source = sqlite3.connect(args.sqlite)
    source.row_factory = sqlite3.Row
    target = psycopg.connect(args.database_url)
    totals: dict[str, int] = {}
    try:
        with target:
            for table in TABLES:
                totals[table] = copy_table(source, target, table)
    finally:
        source.close()
        target.close()
    for table, count in totals.items():
        print(f"{table}: {count}")


if __name__ == "__main__":
    main()
