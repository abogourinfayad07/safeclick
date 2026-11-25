"""Blueprint Render : structure attendue et aucun secret réel."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BLUEPRINT = ROOT / "render.yaml"


def test_blueprint_contains_the_two_expected_services() -> None:
    content = BLUEPRINT.read_text(encoding="utf-8")

    assert "name: safeclick-api" in content
    assert "name: safeclick-web" in content
    assert "healthCheckPath: /health" in content
    assert "dockerfilePath: ./services/api/Dockerfile" in content
    assert "dockerfilePath: ./apps/web/Dockerfile" in content


def test_database_url_is_a_render_secret_not_a_committed_value() -> None:
    content = BLUEPRINT.read_text(encoding="utf-8")

    assert "- key: DATABASE_URL" in content
    assert "sync: false" in content
    assert "postgresql://" not in content
    assert "postgres://" not in content
