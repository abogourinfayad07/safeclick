"""Hachage Argon2id et jetons JWT à usage limité."""

from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError

from app.core.config import settings

_hasher = PasswordHasher()
_DUMMY_HASH = _hasher.hash("dev-only-dummy-password")
_INVALID_TOKEN_ERRORS = (jwt.InvalidTokenError, VerifyMismatchError, VerificationError)


def hash_password(password: str) -> str:
    return _hasher.hash(password)


def verify_password(stored_hash: str, password: str) -> bool:
    candidate = stored_hash or _DUMMY_HASH
    try:
        return _hasher.verify(candidate, password)
    except _INVALID_TOKEN_ERRORS:
        return False


def create_access_token(user_id: str, token_version: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "ver": token_version,
        "purpose": "access",
        "iat": now,
        "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
        "jti": str(uuid4()),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def create_verification_token(user_id: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "purpose": "verify",
        "iat": now,
        "exp": now + timedelta(hours=24),
        "jti": str(uuid4()),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str, expected_purpose: str) -> dict[str, object]:
    payload = jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.jwt_algorithm],
        options={"require": ["exp", "sub", "purpose"]},
    )
    if payload.get("purpose") != expected_purpose:
        raise jwt.InvalidTokenError("Finalité du jeton invalide.")
    return payload


__all__ = [
    "create_access_token",
    "create_verification_token",
    "decode_token",
    "hash_password",
    "verify_password",
]
