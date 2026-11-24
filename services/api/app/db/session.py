"""Moteur SQLAlchemy et gestion du répertoire SQLite local."""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

from .base import Base  # noqa: F401  (exporte la base pour les futures migrations)


def _prepare_sqlite_directory(url: str) -> None:
    """Crée le dossier parent d'une base SQLite locale si nécessaire."""
    parsed = make_url(url)
    if parsed.get_backend_name() != "sqlite":
        return

    database = parsed.database
    if not database or database == ":memory:":
        return

    path = Path(database)
    if not path.is_absolute():
        path = Path.cwd() / path
    path.parent.mkdir(parents=True, exist_ok=True)


_prepare_sqlite_directory(settings.database_url)

_connect_args = (
    {"check_same_thread": False}
    if settings.database_url.startswith("sqlite")
    else {}
)

engine = create_engine(
    settings.database_url,
    connect_args=_connect_args,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

__all__ = ["Base", "SessionLocal", "engine"]
