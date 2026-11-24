"""Historique : un compte ne voit que ses propres analyses."""

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.core.security import create_verification_token
from app.db.session import SessionLocal
from app.models.user import User


def _verified_user(email: str) -> str:
    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.email == email))
        assert user is not None
        return user.id


def _register_verify_login(client: TestClient, email: str) -> str:
    created = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "Motdepasse123!"},
    )
    assert created.status_code == status.HTTP_201_CREATED
    user_id = _verified_user(email)
    client.post(
        "/api/v1/auth/verify",
        json={"token": create_verification_token(user_id)},
    )
    login = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "Motdepasse123!"},
    )
    return login.json()["access_token"]


def test_history_is_scoped_to_the_authenticated_user(client: TestClient) -> None:
    first_token = _register_verify_login(client, "historique-un@example.com")
    second_token = _register_verify_login(client, "historique-deux@example.com")
    first_headers = {"Authorization": f"Bearer {first_token}"}

    submitted = client.post(
        "/api/v1/analyze/url",
        json={"url": "https://www.google.com"},
        headers=first_headers,
    )
    assert submitted.status_code == status.HTTP_200_OK

    first = client.get("/api/v1/analyses", headers=first_headers)
    assert first.status_code == status.HTTP_200_OK
    body = first.json()
    assert body["total"] == 1
    assert body["items"][0]["id"] == submitted.json()["id"]
    assert body["items"][0]["riskLevel"] == "low"
    assert body["items"][0]["engineVersion"] == "rules-v1"

    second = client.get(
        "/api/v1/analyses",
        headers={"Authorization": f"Bearer {second_token}"},
    )
    assert second.status_code == status.HTTP_200_OK
    assert second.json()["total"] == 0


def test_history_requires_authentication(client: TestClient) -> None:
    response = client.get("/api/v1/analyses")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["code"] == "unauthorized"
