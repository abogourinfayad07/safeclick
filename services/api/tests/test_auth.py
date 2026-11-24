"""Authentification Argon2id + JWT et attachement des analyses au compte."""

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_verification_token, verify_password
from app.db.session import SessionLocal
from app.models.analysis import Analysis
from app.models.user import User


def _register(client: TestClient, email: str, password: str = "Motdepasse123!") -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password},
    )
    assert response.status_code == status.HTTP_201_CREATED, response.text


def _verified_user(email: str) -> User:
    with SessionLocal() as db:
        return db.scalar(select(User).where(User.email == email))


def _login(client: TestClient, email: str, password: str = "Motdepasse123!") -> str:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == status.HTTP_200_OK, response.text
    return response.json()["access_token"]


def test_register_login_profile_and_delete_account(client: TestClient) -> None:
    email = "auth-complete@example.com"
    _register(client, email)

    blocked = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "Motdepasse123!"},
    )
    assert blocked.status_code == status.HTTP_403_FORBIDDEN
    assert blocked.json()["code"] == "email_not_verified"

    user = _verified_user(email)
    assert user is not None
    assert user.password_hash != "Motdepasse123!"
    assert verify_password(user.password_hash, "Motdepasse123!") is True

    verification = client.post(
        "/api/v1/auth/verify",
        json={"token": create_verification_token(user.id)},
    )
    assert verification.status_code == status.HTTP_200_OK

    token = _login(client, email)
    headers = {"Authorization": f"Bearer {token}"}

    profile = client.get("/api/v1/user/profile", headers=headers)
    assert profile.status_code == status.HTTP_200_OK
    assert profile.json()["email"] == email
    assert profile.json()["isVerified"] is True

    deletion = client.delete("/api/v1/user/profile", headers=headers)
    assert deletion.status_code == status.HTTP_204_NO_CONTENT


def test_profile_requires_valid_token(client: TestClient) -> None:
    anonymous = client.get("/api/v1/user/profile")
    assert anonymous.status_code == status.HTTP_401_UNAUTHORIZED
    assert anonymous.json()["code"] == "unauthorized"

    invalid = client.get(
        "/api/v1/user/profile",
        headers={"Authorization": "Bearer jeton.invalide.abc"},
    )
    assert invalid.status_code == status.HTTP_401_UNAUTHORIZED
    assert invalid.json()["code"] == "invalid_token"


def test_authenticated_analysis_is_attached_to_user(client: TestClient) -> None:
    email = "auth-analyse@example.com"
    _register(client, email)
    user = _verified_user(email)
    client.post(
        "/api/v1/auth/verify",
        json={"token": create_verification_token(user.id)},
    )
    token = _login(client, email)

    response = client.post(
        "/api/v1/analyze/url",
        json={"url": "https://www.google.com"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK

    with SessionLocal() as db:
        stored = db.scalar(
            select(Analysis).where(Analysis.id == response.json()["id"])
        )
        assert stored is not None
        assert stored.user_id == user.id


def test_duplicate_registration_is_rejected(client: TestClient) -> None:
    email = "auth-doublon@example.com"
    _register(client, email)

    duplicate = client.post(
        "/api/v1/auth/register",
        json={"email": email.upper(), "password": "Motdepasse123!"},
    )
    assert duplicate.status_code == status.HTTP_409_CONFLICT
    assert duplicate.json()["code"] == "email_exists"
