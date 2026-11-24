"""Tests smoke du service et de sa documentation OpenAPI."""

from fastapi.testclient import TestClient


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["database"] == "ok"
    assert payload["environment"] == "test"
    assert payload["version"] == "0.1.0"
    assert "secret" not in payload


def test_openapi_documents_health(client: TestClient) -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/health" in paths
    assert "get" in paths["/health"]


def test_root_returns_service_info(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["name"] == "SAFECLICK API"
