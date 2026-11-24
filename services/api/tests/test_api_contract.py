"""Contrat public de l'API versionnée : santé, information et erreurs."""

from fastapi.testclient import TestClient


def test_health_is_available_with_and_without_prefix(client: TestClient) -> None:
    for path in ("/health", "/api/v1/health"):
        response = client.get(path)

        assert response.status_code == 200
        payload = response.json()
        assert payload["status"] == "ok"
        assert payload["database"] == "ok"
        assert payload["environment"] == "test"
        assert payload["version"] == "0.1.0"


def test_info_exposes_real_limits_and_no_fake_capability(client: TestClient) -> None:
    response = client.get("/api/v1/info")

    assert response.status_code == 200
    payload = response.json()
    assert payload["name"] == "SAFECLICK API"
    assert payload["prefix"] == "/api/v1"
    assert payload["supported_languages"] == ["fr"]
    assert payload["analysis_kinds"] == ["url", "message"]
    assert payload["limits"] == {
        "url_max_length": 2048,
        "message_max_length": 4000,
    }
    assert "garantie" in payload["disclaimer"]


def test_unknown_route_returns_uniform_error(client: TestClient) -> None:
    response = client.get("/api/v1/route-inexistante")

    assert response.status_code == 404
    assert response.json() == {
        "code": "not_found",
        "message": "Ressource introuvable.",
        "details": None,
    }


def test_openapi_uses_distinct_operation_ids(client: TestClient) -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200
    paths = response.json()["paths"]
    assert paths["/health"]["get"]["operationId"] == "health_check"
    assert paths["/api/v1/health"]["get"]["operationId"] == "health_check_v1"
    assert paths["/api/v1/info"]["get"]["operationId"] == "api_info"
