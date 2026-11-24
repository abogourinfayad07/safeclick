"""Sécurité transport, journalisation sans secret et limitation d'abus."""

import logging

from fastapi import status
from fastapi.testclient import TestClient

from app.core.config import settings
from app.core.rate_limit import reset_rate_limiter


def test_security_headers_are_present(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == status.HTTP_200_OK
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["Referrer-Policy"] == "no-referrer"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert "camera=()" in response.headers["Permissions-Policy"]
    assert response.headers["Cache-Control"] == "no-store"
    assert response.headers["Strict-Transport-Security"].startswith("max-age=")


def test_request_logs_never_contain_credentials(client: TestClient, caplog) -> None:  # type: ignore[no-untyped-def]
    secret = "Bearer jeton-ne-jamais-journaliser"

    with caplog.at_level(logging.INFO, logger="safeclick.request"):
        response = client.get(
            "/api/v1/user/profile?secret=ne-pas-ecrire",
            headers={"Authorization": secret},
        )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "jeton-ne-jamais-journaliser" not in caplog.text
    assert "ne-pas-ecrire" not in caplog.text
    assert "/api/v1/user/profile" in caplog.text


def test_rate_limit_returns_uniform_error(client: TestClient, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setattr(settings, "rate_limit_enabled", True)
    monkeypatch.setattr(settings, "rate_limit_per_minute", 2)
    reset_rate_limiter()
    try:
        responses = [
            client.post("/api/v1/analyze/url", json={"url": "https://exemple.fr"})
            for _ in range(3)
        ]

        assert [item.status_code for item in responses] == [
            status.HTTP_200_OK,
            status.HTTP_200_OK,
            status.HTTP_429_TOO_MANY_REQUESTS,
        ]
        assert responses[-1].json()["code"] == "rate_limited"
        assert responses[-1].headers["Retry-After"].isdigit()
    finally:
        reset_rate_limiter()
