"""Dépendances injectées dans les routes."""

from collections.abc import Iterator

from sqlalchemy.orm import Session

from app.db.session import SessionLocal


def get_db() -> Iterator[Session]:
    """Fournit une session SQLAlchemy par requête et la ferme toujours."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
