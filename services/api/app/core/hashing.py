"""Hachage HMAC des contacts signalés : jamais de valeur brute en base."""

import hashlib
import hmac
import unicodedata

from app.core.config import settings


def normalize_contact(value: str, kind: str) -> str:
    """Normalise un contact selon son type avant hachage."""
    cleaned = unicodedata.normalize("NFKC", value).strip()

    if kind == "phone":
        prefix = "+" if cleaned.startswith("+") else ""
        return prefix + "".join(char for char in cleaned if char.isdigit())

    return cleaned.casefold()


def hash_value(value: str, domain: str) -> str:
    """HMAC-SHA256 générique : empêche le hachage inverse trivial."""
    normalized = normalize_contact(value, domain)
    return hmac.new(
        settings.secret_key.encode("utf-8"),
        normalized.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def hash_contact(value: str, kind: str) -> str:
    """Hachage appliqué aux contacts signalés."""
    return hash_value(value, kind)


def hash_api_key(raw_key: str) -> str:
    """HMAC d'une clé API, sensible à la casse (pas de normalisation)."""
    return hmac.new(
        settings.secret_key.encode("utf-8"),
        f"api_key:{raw_key}".encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


__all__ = ["hash_api_key", "hash_contact", "hash_value", "normalize_contact"]
