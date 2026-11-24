"""Profil de l'utilisateur authentifié et suppression de compte."""

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.config import settings
from app.models.user import User
from app.schemas.auth import UserProfile

router = APIRouter(prefix=settings.api_v1_prefix, tags=["users"])


@router.get(
    "/user/profile", response_model=UserProfile, operation_id="get_profile"
)
def get_profile(user: User = Depends(get_current_user)) -> UserProfile:
    return UserProfile(
        email=user.email,
        role=user.role,
        is_verified=user.is_verified,
        created_at=user.created_at,
    )


@router.delete(
    "/user/profile",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="delete_account",
)
def delete_account(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> Response:
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
