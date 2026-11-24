"""La migration initiale doit produire le schéma réel attendu."""

import os
import subprocess
import sys
from pathlib import Path

from sqlalchemy import create_engine, inspect

REPO_ROOT = Path(__file__).resolve().parents[3]
CONFIG_PATH = REPO_ROOT / "services" / "api" / "alembic.ini"


def test_alembic_creates_initial_schema(tmp_path: Path) -> None:
    database_path = tmp_path / "migration.db"
    database_url = f"sqlite:///{database_path.as_posix()}"

    env = os.environ.copy()
    env.update(
        {
            "ENVIRONMENT": "test",
            "DATABASE_URL": database_url,
            "SECRET_KEY": "test-only-placeholder-key-longer-than-thirty-two-bytes",
        }
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "alembic",
            "-c",
            str(CONFIG_PATH),
            "upgrade",
            "head",
        ],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    inspector = inspect(create_engine(database_url))
    assert {"users", "analyses", "reports", "api_keys", "alembic_version"}.issubset(
        set(inspector.get_table_names())
    )

    report_columns = {column["name"] for column in inspector.get_columns("reports")}
    assert {"contact_hash", "reason_code", "status"}.issubset(report_columns)

    user_columns = {column["name"] for column in inspector.get_columns("users")}
    assert "plan" in user_columns

    user_indexes = {
        index["name"]: index["unique"] for index in inspector.get_indexes("users")
    }
    assert bool(user_indexes.get("ix_users_email")) is True
    assert bool(user_indexes.get("ix_users_plan")) is False

    key_columns = {column["name"] for column in inspector.get_columns("api_keys")}
    assert {"key_hash", "daily_quota", "usage_count", "revoked_at"}.issubset(key_columns)
