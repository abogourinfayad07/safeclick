"""Dépendances injectées dans les routes : base, authentification, rôles."""

from collections.abc import Iterator

import jwt
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.api.errors import ApiError
from app.core.security import decode_token
from app.db.session import SessionLocal
from app.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)


def get_db() -> Iterator[Session]:
    """Fournit une session SQLAlchemy par requête et la ferme toujours."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _credentials_from_header(credentials: HTTPAuthorizationCredentials | None) -> str:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise ApiError(
            status_code=401,
            code="unauthorized",
            message="Authentification requise.",
        )
    return credentials.credentials


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    token = _credentials_from_header(credentials)
    try:
        payload = decode_token(token, "access")
    except jwt.InvalidTokenError as exc:
        raise ApiError(
            status_code=401,
            code="invalid_token",
            message="Jeton invalide ou expiré.",
        ) from exc

    user = db.get(User, str(payload.get("sub", "")))
    if (
        user is None
        or not user.is_verified
        or user.token_version != payload.get("ver")
    ):
        raise ApiError(
            status_code=401,
            code="invalid_token",
            message="Jeton invalide ou compte indisponible.",
        )
    return user


def get_optional_user(
    request: Request,
    db: Session = Depends(get_db),
) -> User | None:
    """Attache un utilisateur si un jeton valide est fourni, sinon reste anonyme."""
    header = request.headers.get("authorization", "")
    if not header.lower().startswith("bearer "):
        return None

    token = header.split(" ", 1)[1].strip()
    try:
        payload = decode_token(token, "access")
    except jwt.InvalidTokenError:
        return None

    user = db.get(User, str(payload.get("sub", "")))
    if user is None or not user.is_verified:
        return None
    if user.token_version != payload.get("ver"):
        return None
    return user


def get_current_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise ApiError(
            status_code=403,
            code="forbidden",
            message="Accès réservé aux administrateurs.",
        )
    return user
