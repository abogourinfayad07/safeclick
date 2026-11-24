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


def hash_contact(value: str, kind: str) -> str:
    """HMAC-SHA256 : le secret applicatif empêche le hachage inverse trivial."""
    normalized = normalize_contact(value, kind)
    return hmac.new(
        settings.secret_key.encode("utf-8"),
        normalized.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


__all__ = ["hash_contact", "normalize_contact"]
