"""Normalisation et hachage HMAC des contacts signalés."""

import hashlib

from app.core.hashing import hash_contact, normalize_contact


def test_phone_normalization_keeps_only_digits_and_plus() -> None:
    assert normalize_contact("+33 6 12 34 56 78", "phone") == "+33612345678"
    assert normalize_contact("06 12 34 56 78", "phone") == "0612345678"


def test_email_and_url_are_casefolded() -> None:
    assert normalize_contact("  User@Example.COM ", "email") == "user@example.com"
    assert normalize_contact("HTTPS://Exemple.FR/Page", "url") == "https://exemple.fr/page"


def test_hash_is_stable_and_not_a_plain_sha256() -> None:
    first = hash_contact("user@example.com", "email")
    second = hash_contact("  USER@example.com ", "email")

    assert first == second
    assert len(first) == 64
    assert "user@example.com" not in first
    assert first != hashlib.sha256(b"user@example.com").hexdigest()
