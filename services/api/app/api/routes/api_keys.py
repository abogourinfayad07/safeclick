"""Gestion des clés API de l'utilisateur authentifié."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.config import settings
from app.models.user import User
from app.schemas.api_key import ApiKeyCreate, ApiKeyCreated, ApiKeyItem, ApiKeyList
from app.services.api_keys import create_api_key, list_api_keys, revoke_api_key

router = APIRouter(prefix=settings.api_v1_prefix, tags=["api-keys"])

_NOTICE = "Copiez cette clé maintenant : elle n'est affichée qu'une seule fois."


@router.post(
    "/api-keys",
    response_model=ApiKeyCreated,
    status_code=status.HTTP_201_CREATED,
    operation_id="create_api_key",
)
def create_key(
    payload: ApiKeyCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ApiKeyCreated:
    key, raw_key = create_api_key(db, user, payload.name)
    return ApiKeyCreated(
        id=key.id,
        name=key.name,
        prefix=key.prefix,
        key=raw_key,
        dailyQuota=key.daily_quota,
        createdAt=key.created_at,
        notice=_NOTICE,
    )


@router.get("/api-keys", response_model=ApiKeyList, operation_id="list_api_keys")
def list_keys(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ApiKeyList:
    return ApiKeyList(
        items=[
            ApiKeyItem(
                id=key.id,
                name=key.name,
                prefix=key.prefix,
                dailyQuota=key.daily_quota,
                usageCount=key.usage_count,
                createdAt=key.created_at,
                revokedAt=key.revoked_at,
            )
            for key in list_api_keys(db, user)
        ]
    )


@router.delete(
    "/api-keys/{key_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="revoke_api_key",
)
def revoke_key(
    key_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> None:
    revoke_api_key(db, user, key_id)
