"""Signalements : validation stricte, hachage et absence d'accusation."""

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.hashing import hash_contact
from app.db.session import SessionLocal
from app.models.report import Report


def payload(email: str = "signalement@example.com") -> dict[str, object]:
    return {
        "contact_kind": "email",
        "contact": email,
        "reason_code": "urgency",
        "acknowledge_unverified": True,
    }


def test_create_report_stores_only_hashed_contact(client: TestClient) -> None:
    raw_contact = "victime@example.com"

    response = client.post("/api/v1/reports", json=payload(raw_contact))

    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body["status"] == "unverified"
    assert "accusation" in body["disclaimer"]
    assert raw_contact not in response.text

    with SessionLocal() as db:
        stored = db.get(Report, body["id"])
        assert stored is not None
        assert stored.contact_hash == hash_contact(raw_contact, "email")
        assert stored.contact_hash != raw_contact
        assert not hasattr(stored, "contact")


def test_duplicate_report_reuses_existing_record(client: TestClient) -> None:
    first = client.post("/api/v1/reports", json=payload("doublon@example.com"))
    second = client.post("/api/v1/reports", json=payload("  DOUBLON@example.com "))

    assert first.status_code == status.HTTP_201_CREATED
    assert second.status_code == status.HTTP_201_CREATED
    assert second.json()["id"] == first.json()["id"]
    assert "déjà" in second.json()["message"]

    expected_hash = hash_contact("doublon@example.com", "email")
    with SessionLocal() as db:
        count = db.scalar(
            select(func.count())
            .select_from(Report)
            .where(Report.contact_hash == expected_hash)
        )
        assert count == 1


def test_invalid_contact_returns_uniform_validation_error(client: TestClient) -> None:
    response = client.post("/api/v1/reports", json=payload("short"))

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    body = response.json()
    assert body["code"] == "validation_error"
    fields = {detail["field"] for detail in body["details"]}
    assert "contact" in fields


def test_extra_field_is_rejected(client: TestClient) -> None:
    data = payload("champ-supplementaire@example.com")
    data["unexpected"] = "champ interdit"

    response = client.post("/api/v1/reports", json=data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    body = response.json()
    assert body["code"] == "validation_error"
    fields = {detail["field"] for detail in body["details"]}
    assert "unexpected" in fields


def test_report_requires_unverified_acknowledgement(client: TestClient) -> None:
    data = payload("consentement@example.com")
    data["acknowledge_unverified"] = False

    response = client.post("/api/v1/reports", json=data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json()["code"] == "validation_error"
