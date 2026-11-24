"""Informations publiques sur l'API, utilisables par les clients web et mobile."""

from fastapi import APIRouter

from app.api.errors import ApiError
from app.core.config import settings
from app.core.limits import MESSAGE_MAX_LENGTH, URL_MAX_LENGTH
from app.core.version import API_VERSION
from app.schemas.common import ApiInfoResponse, ApiLimits

router = APIRouter(prefix=settings.api_v1_prefix, tags=["info"])


@router.get("/info", response_model=ApiInfoResponse, operation_id="api_info")
def api_info() -> ApiInfoResponse:
    if settings.is_development is False and settings.secret_key.startswith("dev-only"):
        # Configuration incomplète en production : on refuse de répondre plutôt
        # que de laisser une clé de développement en ligne.
        raise ApiError(
            status_code=503,
            code="misconfigured",
            message="Configuration serveur incomplète.",
        )

    return ApiInfoResponse(
        name="SAFECLICK API",
        version=API_VERSION,
        prefix=settings.api_v1_prefix,
        supported_languages=["fr"],
        analysis_kinds=["url", "message"],
        limits=ApiLimits(
            url_max_length=URL_MAX_LENGTH,
            message_max_length=MESSAGE_MAX_LENGTH,
        ),
        disclaimer=(
            "Les résultats sont indicatifs. Un risque faible n'est jamais "
            "une garantie de sécurité."
        ),
    )
