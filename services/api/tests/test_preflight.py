"""Pré-vérification : accepte les URL PostgreSQL/Neon telles que fournies."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import preflight  # noqa: E402


def _deploy_env(**overrides: str) -> dict[str, str]:
    values: dict[str, str] = {
        "ENVIRONMENT": "production",
        "SECRET_KEY": "preflight-test-secret-longer-than-thirty-two-chars",
        "SITE_URL": "https://safeclick.example",
        "NEXT_PUBLIC_API_URL": "https://api.safeclick.example",
        "DATABASE_URL": "postgresql+psycopg://user:pass@db.example/neondb",
        "EMAIL_BACKEND": "smtp",
        "RATE_LIMIT_ENABLED": "true",
    }
    values.update(overrides)
    return values


def test_neon_url_is_accepted_by_preflight() -> None:
    url = "postgres://user:pass@ep-test.neon.tech/neondb?sslmode=require"

    assert preflight.check_deploy_env(_deploy_env(DATABASE_URL=url)) == []


def test_sqlite_is_still_refused_by_preflight() -> None:
    problems = preflight.check_deploy_env(
        _deploy_env(DATABASE_URL="sqlite:///./data/safeclick.db")
    )

    assert any("DATABASE_URL" in problem for problem in problems)
