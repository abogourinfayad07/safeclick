"""Détecteurs déterministes : signaux explicites et classification."""

from app.detectors.message import analyze_message
from app.detectors.url import analyze_url
from app.models.enums import RiskLevel


def test_benign_url_has_no_signal() -> None:
    result = analyze_url("https://www.google.com")

    assert result["indicators"] == []
    assert result["score"] == 0
    assert result["risk_level"] is RiskLevel.LOW


def test_suspicious_url_reports_explanations() -> None:
    result = analyze_url(
        "http://paypal.secure-login.example.com/verify?code=123456"
    )

    codes = {indicator.code for indicator in result["indicators"]}
    assert {"insecure_scheme", "brand_in_subdomain", "sensitive_query"} <= codes
    assert result["risk_level"] is not RiskLevel.LOW
    assert any("garantie" in item for item in result["limitations"])


def test_punycode_is_flagged() -> None:
    result = analyze_url("https://xn--exemple-tza.com")

    assert "punycode" in {indicator.code for indicator in result["indicators"]}


def test_benign_message_has_no_signal() -> None:
    result = analyze_message(
        "Bonjour, voici le document dont on a parlé ce matin. À bientôt."
    )

    assert result["indicators"] == []
    assert result["risk_level"] is RiskLevel.LOW


def test_phishing_message_is_high_risk() -> None:
    result = analyze_message(
        "URGENT!!! Votre compte sera bloqué. Envoyez votre code OTP et "
        "votre mot de passe à votre banque par mail immédiatement. "
        "Cliquez ici : https://bit.ly/abc123"
    )

    codes = {indicator.code for indicator in result["indicators"]}
    assert {
        "urgency",
        "code_request",
        "impersonation",
        "threat",
        "embedded_link",
        "private_contact",
    } <= codes
    assert result["score"] >= 60
    assert result["risk_level"] is RiskLevel.HIGH
