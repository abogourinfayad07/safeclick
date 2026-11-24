"""Sauvegarde SQLite réelle et refus explicite des autres moteurs."""

import sqlite3
from pathlib import Path

import pytest

from app.core.config import settings
from app.ops.backup import backup_database


def test_sqlite_backup_preserves_data(tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    source = tmp_path / "source.db"
    with sqlite3.connect(source) as connection:
        connection.execute("CREATE TABLE note (value TEXT)")
        connection.execute("INSERT INTO note (value) VALUES (?)", ("conservé",))

    monkeypatch.setattr(settings, "database_url", f"sqlite:///{source.as_posix()}")

    destination = backup_database(tmp_path / "backups" / "copie.db")

    assert destination.is_file()
    with sqlite3.connect(destination) as connection:
        value = connection.execute("SELECT value FROM note").fetchone()[0]
    assert value == "conservé"


def test_non_sqlite_backup_is_refused(tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setattr(
        settings,
        "database_url",
        "postgresql+psycopg://utilisateur:motdepasse@localhost:5432/safeclick",
    )

    with pytest.raises(RuntimeError, match="PostgreSQL"):
        backup_database(tmp_path / "copie.db")
