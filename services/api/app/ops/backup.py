"""Sauvegarde cohérente de la base SQLite de développement.

PostgreSQL en production doit être sauvegardé par l'outil de l'hébergeur :
cette commande refuse explicitement les autres moteurs plutôt que de simuler
une sauvegarde.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy.engine import make_url

from app.core.config import settings

ROOT = Path(__file__).resolve().parents[4]
BACKUP_DIR = ROOT / "backups"


def backup_database(destination: Path | None = None) -> Path:
    url = make_url(settings.database_url)
    if url.get_backend_name() != "sqlite" or not url.database or url.database == ":memory:":
        raise RuntimeError(
            "Cette commande ne sauvegarde que les bases SQLite fichier. "
            "Utilisez l'outil de sauvegarde de l'hébergeur pour PostgreSQL."
        )

    source = Path(url.database)
    if not source.is_absolute():
        source = ROOT / source
    if not source.is_file():
        raise FileNotFoundError(f"Base introuvable : {source}")

    if destination is None:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        destination = BACKUP_DIR / f"safeclick-{stamp}.db"
    destination.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(source) as origin, sqlite3.connect(destination) as target:
        origin.backup(target)
    return destination


def main() -> None:
    path = backup_database()
    print(f"Sauvegarde créée : {path}")


if __name__ == "__main__":
    main()
