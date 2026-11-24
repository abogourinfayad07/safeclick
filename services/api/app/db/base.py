"""Base déclarative SQLAlchemy partagée par tous les modèles."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Classe de base des modèles ORM."""
