"""Configuration de la base : URL Neon, TLS et refus de SQLite en production."""

import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_neon_url_uses_psycopg_and_requires_tls(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setenv(
        "DATABASE_URL", "postgres://utilisateur:motdepasse@ep-test.neon.tech/neondb"
    )

    config = Settings(_env_file=None)

    assert config.database_url.startswith("postgresql+psycopg://")
    assert "sslmode=require" in config.database_url


def test_explicit_ssl_mode_is_kept(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+psycopg://utilisateur:motdepasse@ep-test.neon.tech/neondb?sslmode=verify-full",
    )

    config = Settings(_env_file=None)

    assert "sslmode=verify-full" in config.database_url
    assert "sslmode=require" not in config.database_url


def test_sqlite_is_refused_in_production(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./data/safeclick.db")

    with pytest.raises(ValidationError, match="SQLite est interdit"):
        Settings(_env_file=None)
