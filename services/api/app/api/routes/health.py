"""Endpoints de santé : service et connexion à la base, en v1 et sans préfixe."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.config import settings
from app.core.version import API_VERSION
from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])
v1_router = APIRouter(prefix=settings.api_v1_prefix, tags=["health"])


def _health_payload(db: Session) -> HealthResponse:
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        # Aucun détail technique n'est renvoyé au client.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable",
        ) from exc

    return HealthResponse(
        status="ok",
        database="ok",
        environment=settings.environment,
        version=API_VERSION,
    )


@router.get("/health", response_model=HealthResponse, operation_id="health_check")
def health(db: Session = Depends(get_db)) -> HealthResponse:
    return _health_payload(db)


@v1_router.get(
    "/health", response_model=HealthResponse, operation_id="health_check_v1"
)
def health_v1(db: Session = Depends(get_db)) -> HealthResponse:
    return _health_payload(db)
