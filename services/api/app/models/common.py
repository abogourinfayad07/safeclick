"""Utilitaires partagés par les modèles SQLAlchemy."""

from datetime import datetime, timezone
from uuid import uuid4


def new_id() -> str:
    """Identifiant texte compatible SQLite et PostgreSQL."""
    return str(uuid4())


def utcnow() -> datetime:
    """Horodatage UTC conscient."""
    return datetime.now(timezone.utc)
