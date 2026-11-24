"""Création, révocation et consommation des clés API."""

from __future__ import annotations

import secrets
from datetime import date

from fastapi import status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.errors import ApiError
from app.core.hashing import hash_api_key
from app.core.plans import plan_by_code
from app.models.api_key import ApiKey
from app.models.common import utcnow
from app.models.user import User


def _active_key_count(db: Session, user_id: str) -> int:
    return int(
        db.scalar(
            select(func.count())
            .select_from(ApiKey)
            .where(ApiKey.user_id == user_id, ApiKey.revoked_at.is_(None))
        )
        or 0
    )


def create_api_key(db: Session, user: User, name: str) -> tuple[ApiKey, str]:
    plan = plan_by_code(user.plan)
    if plan is None:
        raise ApiError(
            status_code=status.HTTP_409_CONFLICT,
            code="invalid_plan",
            message="Offre indisponible.",
        )
    limit = int(plan["apiKeys"])
    if _active_key_count(db, user.id) >= limit:
        raise ApiError(
            status_code=status.HTTP_409_CONFLICT,
            code="api_key_limit_reached",
            message="Nombre maximal de clés API atteint pour votre offre.",
        )

    raw_key = f"sc_{secrets.token_urlsafe(32)}"
    key = ApiKey(
        user_id=user.id,
        name=name.strip(),
        prefix=raw_key[:11],
        key_hash=hash_api_key(raw_key),
        daily_quota=int(plan["dailyAnalyses"]),
        created_at=utcnow(),
    )
    db.add(key)
    db.commit()
    db.refresh(key)
    return key, raw_key


def list_api_keys(db: Session, user: User) -> list[ApiKey]:
    return list(
        db.scalars(
            select(ApiKey).where(ApiKey.user_id == user.id).order_by(ApiKey.created_at.desc())
        )
    )


def revoke_api_key(db: Session, user: User, key_id: str) -> None:
    key = db.get(ApiKey, key_id)
    if key is None or key.user_id != user.id:
        raise ApiError(
            status_code=status.HTTP_404_NOT_FOUND,
            code="not_found",
            message="Clé API introuvable.",
        )
    if key.revoked_at is None:
        key.revoked_at = utcnow()
        db.commit()


def consume_api_key(db: Session, raw_key: str) -> tuple[User, ApiKey]:
    """Authentifie une clé et consomme une unité du quota journalier."""
    key = db.scalar(
        select(ApiKey).where(
            ApiKey.key_hash == hash_api_key(raw_key),
            ApiKey.revoked_at.is_(None),
        )
    )
    if key is None:
        raise ApiError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="invalid_api_key",
            message="Clé API invalide ou révoquée.",
        )

    user = db.get(User, key.user_id)
    if user is None or not user.is_verified:
        raise ApiError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="invalid_api_key",
            message="Clé API invalide ou compte indisponible.",
        )

    today = date.today()
    if key.usage_date != today:
        key.usage_date = today
        key.usage_count = 0
        db.commit()

    if key.usage_count >= key.daily_quota:
        raise ApiError(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            code="quota_exceeded",
            message="Quota quotidien de la clé API épuisé.",
        )

    key.usage_count += 1
    key.last_used_at = utcnow()
    db.commit()
    return user, key
