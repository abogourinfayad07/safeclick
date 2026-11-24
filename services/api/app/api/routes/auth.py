"""Inscription, vérification en console et connexion JWT."""

import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.errors import ApiError
from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_verification_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
    VerifyRequest,
)

logger = logging.getLogger("safeclick.api.auth")
router = APIRouter(prefix=settings.api_v1_prefix, tags=["auth"])


@router.post(
    "/auth/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    operation_id="register_user",
)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> RegisterResponse:
    existing = db.scalar(select(User).where(User.email == payload.email))
    if existing is not None:
        raise ApiError(
            status_code=status.HTTP_409_CONFLICT,
            code="email_exists",
            message="Un compte existe déjà avec cette adresse.",
        )

    user = User(email=payload.email, password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    verification_token = create_verification_token(user.id)
    if settings.email_backend == "console" and settings.is_development:
        logger.info(
            "Vérification SAFECLICK (développement) : %s/api/v1/auth/verify",
            settings.site_url,
        )
        logger.info("Jeton de vérification (dev uniquement) : %s", verification_token)

    return RegisterResponse(
        email=user.email,
        message="Compte créé. Vérifiez votre adresse avant de vous connecter.",
        verification_required=True,
    )


@router.post(
    "/auth/verify",
    response_model=RegisterResponse,
    operation_id="verify_email",
)
def verify_email(payload: VerifyRequest, db: Session = Depends(get_db)) -> RegisterResponse:
    from jwt import InvalidTokenError

    try:
        claims = decode_token(payload.token, "verify")
    except InvalidTokenError as exc:
        raise ApiError(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="invalid_verification_token",
            message="Lien de vérification invalide ou expiré.",
        ) from exc

    user = db.get(User, str(claims.get("sub", "")))
    if user is None:
        raise ApiError(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="invalid_verification_token",
            message="Lien de vérification invalide ou expiré.",
        )

    if not user.is_verified:
        user.is_verified = True
        db.commit()
        db.refresh(user)

    return RegisterResponse(
        email=user.email,
        message="Adresse vérifiée. Vous pouvez vous connecter.",
        verification_required=False,
    )


@router.post("/auth/login", response_model=TokenResponse, operation_id="login")
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.scalar(select(User).where(User.email == payload.email))

    if user is None or not verify_password(user.password_hash, payload.password):
        raise ApiError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="invalid_credentials",
            message="Adresse ou mot de passe incorrect.",
        )
    if not user.is_verified:
        raise ApiError(
            status_code=status.HTTP_403_FORBIDDEN,
            code="email_not_verified",
            message="Vérifiez votre adresse e-mail avant de vous connecter.",
        )

    return TokenResponse(
        access_token=create_access_token(user.id, user.token_version),
        expires_in=settings.access_token_expire_minutes * 60,
    )
