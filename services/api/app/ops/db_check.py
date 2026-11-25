"""Vérifie la connexion à la base sans jamais afficher le mot de passe."""

from __future__ import annotations

from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

from app.core.config import settings


def main() -> int:
    url = make_url(settings.database_url)
    backend = url.get_backend_name()
    target = f"{backend}://{url.host or 'local'}/{url.database or ''}"

    engine = create_engine(settings.database_url, pool_pre_ping=True)
    try:
        with engine.connect() as connection:
            result = connection.scalar(text("SELECT 1"))
            server_version = (
                connection.scalar(text("SHOW server_version")) if backend == "postgresql" else None
            )
        print(f"Connexion OK : {target}")
        print(f"SELECT 1 -> {result}")
        if server_version:
            print(f"Version PostgreSQL -> {server_version}")
        return 0
    except Exception as exc:
        # Les exceptions SQLAlchemy peuvent contenir des détails de connexion :
        # on affiche uniquement le type, jamais le message brut.
        print(f"Connexion échouée ({type(exc).__name__}). Vérifiez DATABASE_URL côté serveur.")
        return 1
    finally:
        engine.dispose()


if __name__ == "__main__":
    raise SystemExit(main())
