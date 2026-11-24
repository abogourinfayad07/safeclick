"""Offres, quotas de clés API et absence de paiement actif."""

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_verification_token
from app.db.session import SessionLocal
from app.models.api_key import ApiKey
from app.models.user import User


def _auth_headers(client: TestClient, email: str) -> dict[str, str]:
    registration = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "Motdepasse123!"},
    )
    assert registration.status_code == status.HTTP_201_CREATED, registration.text

    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.email == email))
        assert user is not None
        verification_token = create_verification_token(user.id)

    client.post("/api/v1/auth/verify", json={"token": verification_token})
    login = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "Motdepasse123!"},
    )
    assert login.status_code == status.HTTP_200_OK, login.text
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def test_public_plans_have_no_active_payment(client: TestClient) -> None:
    response = client.get("/api/v1/billing/plans")

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["paymentActive"] is False
    assert [plan["code"] for plan in body["plans"]] == ["free", "pro", "business"]
    assert body["plans"][0]["dailyAnalyses"] == 50
    assert body["plans"][1]["priceLabel"] == "Sur devis"


def test_subscription_uses_real_user_plan(client: TestClient) -> None:
    headers = _auth_headers(client, "abonnement@example.com")

    response = client.get("/api/v1/billing/subscription", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["plan"] == "free"
    assert body["planName"] == "FREE"
    assert body["paymentActive"] is False


def test_api_key_is_shown_once_then_usable_and_revocable(client: TestClient) -> None:
    headers = _auth_headers(client, "cles@example.com")

    created = client.post(
        "/api/v1/api-keys",
        json={"name": "Intégration locale"},
        headers=headers,
    )
    assert created.status_code == status.HTTP_201_CREATED, created.text
    body = created.json()
    raw_key = body["key"]
    assert raw_key.startswith("sc_")
    assert body["prefix"] == raw_key[:11]
    assert "n'est affichée qu'une seule fois" in body["notice"]

    with SessionLocal() as db:
        stored = db.get(ApiKey, body["id"])
        assert stored is not None
        assert stored.key_hash != raw_key

    listed = client.get("/api/v1/api-keys", headers=headers)
    assert listed.status_code == status.HTTP_200_OK
    assert raw_key not in listed.text
    item = listed.json()["items"][0]
    assert item["dailyQuota"] == 50
    assert item["usageCount"] == 0

    analysis = client.post(
        "/api/v1/analyze/url",
        json={"url": "https://www.google.com"},
        headers={"X-API-Key": raw_key},
    )
    assert analysis.status_code == status.HTTP_200_OK

    listed_again = client.get("/api/v1/api-keys", headers=headers)
    assert listed_again.json()["items"][0]["usageCount"] == 1

    revoked = client.delete(f"/api/v1/api-keys/{body['id']}", headers=headers)
    assert revoked.status_code == status.HTTP_204_NO_CONTENT

    refused = client.post(
        "/api/v1/analyze/url",
        json={"url": "https://www.google.com"},
        headers={"X-API-Key": raw_key},
    )
    assert refused.status_code == status.HTTP_401_UNAUTHORIZED
    assert refused.json()["code"] == "invalid_api_key"


def test_api_key_daily_quota_is_enforced(client: TestClient) -> None:
    headers = _auth_headers(client, "quota@example.com")
    created = client.post(
        "/api/v1/api-keys",
        json={"name": "Quota réduit"},
        headers=headers,
    )
    key_id = created.json()["id"]
    raw_key = created.json()["key"]

    with SessionLocal() as db:
        key = db.get(ApiKey, key_id)
        assert key is not None
        key.daily_quota = 1
        db.commit()

    payload = {"url": "https://www.google.com"}
    first = client.post("/api/v1/analyze/url", json=payload, headers={"X-API-Key": raw_key})
    second = client.post("/api/v1/analyze/url", json=payload, headers={"X-API-Key": raw_key})

    assert first.status_code == status.HTTP_200_OK
    assert second.status_code == status.HTTP_429_TOO_MANY_REQUESTS
    assert second.json()["code"] == "quota_exceeded"


def test_free_plan_limits_active_api_keys(client: TestClient) -> None:
    headers = _auth_headers(client, "limite-cles@example.com")

    created = client.post(
        "/api/v1/api-keys",
        json={"name": "Clé unique FREE"},
        headers=headers,
    )
    assert created.status_code == status.HTTP_201_CREATED

    refused = client.post(
        "/api/v1/api-keys",
        json={"name": "Clé surnuméraire"},
        headers=headers,
    )
    assert refused.status_code == status.HTTP_409_CONFLICT
    assert refused.json()["code"] == "api_key_limit_reached"
