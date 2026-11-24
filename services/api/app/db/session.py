"""Moteur SQLAlchemy et gestion du répertoire SQLite local."""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings

from .base import Base  # noqa: F401  (exporte la base pour les migrations)


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

_is_sqlite = settings.database_url.startswith("sqlite")
_is_memory = settings.database_url in {"sqlite:///:memory:", "sqlite://"}

_engine_options: dict[str, object] = {"pool_pre_ping": True}
if _is_sqlite:
    _engine_options["connect_args"] = {"check_same_thread": False}
if _is_memory:
    # Une seule connexion partagée : les tests HTTP et les threads FastAPI
    # voient exactement le même schéma en mémoire.
    _engine_options["poolclass"] = StaticPool

engine = create_engine(settings.database_url, **_engine_options)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

__all__ = ["Base", "SessionLocal", "engine"]
