"""Administration : seuls les admins modèrent, statistiques mesurées sur la base."""

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.core.security import create_verification_token
from app.db.session import SessionLocal
from app.models.report import Report
from app.models.user import User


def _admin_token(client: TestClient, email: str) -> str:
    created = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "Motdepasse123!"},
    )
    assert created.status_code == status.HTTP_201_CREATED

    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.email == email))
        assert user is not None
        user.is_verified = True
        user.role = "admin"
        db.commit()
        token_user_id = user.id

    client.post(
        "/api/v1/auth/verify",
        json={"token": create_verification_token(token_user_id)},
    )
    login = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "Motdepasse123!"},
    )
    assert login.status_code == status.HTTP_200_OK
    return login.json()["access_token"]


def _user_token(client: TestClient, email: str) -> str:
    created = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "Motdepasse123!"},
    )
    assert created.status_code == status.HTTP_201_CREATED
    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.email == email))
        assert user is not None
        user_id = user.id
    client.post(
        "/api/v1/auth/verify",
        json={"token": create_verification_token(user_id)},
    )
    login = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "Motdepasse123!"},
    )
    return login.json()["access_token"]


def test_non_admin_cannot_access_reports(client: TestClient) -> None:
    token = _user_token(client, "admin-refuse@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/v1/admin/reports", headers=headers)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["code"] == "forbidden"


def test_admin_can_review_a_report_and_see_real_stats(client: TestClient) -> None:
    admin_token = _admin_token(client, "admin-ok@example.com")
    headers = {"Authorization": f"Bearer {admin_token}"}

    submitted = client.post(
        "/api/v1/reports",
        json={
            "contact_kind": "email",
            "contact": "moderation@example.com",
            "reason_code": "urgency",
            "acknowledge_unverified": True,
        },
    )
    assert submitted.status_code == status.HTTP_201_CREATED
    report_id = submitted.json()["id"]

    listed = client.get("/api/v1/admin/reports", headers=headers)
    assert listed.status_code == status.HTTP_200_OK
    assert listed.json()["total"] >= 1
    assert any(item["id"] == report_id for item in listed.json()["items"])

    reviewed = client.post(
        f"/api/v1/admin/reports/{report_id}/review",
        json={"status": "confirmed"},
        headers=headers,
    )
    assert reviewed.status_code == status.HTTP_200_OK
    assert reviewed.json()["status"] == "confirmed"
    assert reviewed.json()["reviewedAt"]

    with SessionLocal() as db:
        stored = db.get(Report, report_id)
        assert stored is not None
        assert stored.status.value == "confirmed"
        assert stored.moderator_id

    stats = client.get("/api/v1/admin/stats", headers=headers)
    assert stats.status_code == status.HTTP_200_OK
    payload = stats.json()
    assert payload["reports"]["confirmed"] >= 1
    assert payload["analyses"]["low"] >= 0
    assert "métriques de performance" in payload["note"]


def test_review_rejects_unknown_status_and_missing_report(client: TestClient) -> None:
    headers = {"Authorization": f"Bearer {_admin_token(client, 'admin-validation@example.com')}"}

    invalid = client.post(
        "/api/v1/admin/reports/inconnu/review",
        json={"status": "confirmed"},
        headers=headers,
    )
    assert invalid.status_code == status.HTTP_404_NOT_FOUND

    invalid_status = client.post(
        "/api/v1/admin/reports/inconnu/review",
        json={"status": "inconnu"},
        headers=headers,
    )
    assert invalid_status.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
