"""Routes d'analyse : contrat camelCase et persistance sans contenu brut."""

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.hashing import hash_value
from app.db.session import SessionLocal
from app.models.analysis import Analysis


def test_analyze_url_route_persists_summary(client: TestClient) -> None:
    url = "https://www.google.com"

    response = client.post("/api/v1/analyze/url", json={"url": url})

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["kind"] == "url"
    assert body["riskLevel"] == "low"
    assert body["score"] == 0
    assert body["createdAt"]
    assert isinstance(body["indicators"], list)

    with SessionLocal() as db:
        stored = db.scalar(
            select(Analysis).where(Analysis.input_hash == hash_value(url, "analysis"))
        )
        assert stored is not None
        assert stored.input_preview == url
        assert stored.input_hash != url
        assert stored.engine_version == "rules-v1"


def test_analyze_message_route_returns_explanations(client: TestClient) -> None:
    message = "URGENT : envoyez votre code OTP à votre banque immédiatement."

    response = client.post("/api/v1/analyze/message", json={"message": message})

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["kind"] == "message"
    assert body["riskLevel"] in {"medium", "high"}
    assert body["indicators"]
    assert all("detail" in item for item in body["indicators"])
    assert body["limitations"]

    with SessionLocal() as db:
        stored = db.scalar(
            select(Analysis).where(Analysis.input_hash == hash_value(message, "analysis"))
        )
        assert stored is not None
        assert stored.engine_version == "rules-v1+nb-fr-v1"


def test_analysis_input_is_strictly_validated(client: TestClient) -> None:
    response = client.post(
        "/api/v1/analyze/url",
        json={"url": "https://exemple.fr", "unexpected": True},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json()["code"] == "validation_error"
