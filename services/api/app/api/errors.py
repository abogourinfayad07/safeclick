"""Réponses d'erreur uniformes, sans fuite de détails techniques."""

import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.schemas.common import ErrorField, ErrorResponse

logger = logging.getLogger("safeclick.api")


class ApiError(Exception):
    """Erreur métier explicite, traduite en JSON par l'API."""

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: list[ErrorField] | None = None,
    ) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details
        super().__init__(message)


def _json_error(
    status_code: int,
    code: str,
    message: str,
    details: list[ErrorField] | None = None,
) -> JSONResponse:
    payload = ErrorResponse(code=code, message=message, details=details)
    return JSONResponse(status_code=status_code, content=payload.model_dump())


async def api_error_handler(_request: Request, exc: ApiError) -> JSONResponse:
    return _json_error(exc.status_code, exc.code, exc.message, exc.details)


async def validation_error_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    details: list[ErrorField] = []
    for error in exc.errors():
        parts = [
            str(part)
            for part in error.get("loc", ())
            if part not in {"body", "query", "path", "header"}
        ]
        details.append(
            ErrorField(
                field=".".join(parts) or "request",
                message=str(error.get("msg", "Valeur invalide")),
            )
        )
    return _json_error(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        code="validation_error",
        message="Données invalides.",
        details=details,
    )


async def http_exception_handler(
    _request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    code_by_status = {
        status.HTTP_404_NOT_FOUND: "not_found",
        status.HTTP_405_METHOD_NOT_ALLOWED: "method_not_allowed",
        status.HTTP_413_CONTENT_TOO_LARGE: "payload_too_large",
        status.HTTP_429_TOO_MANY_REQUESTS: "rate_limited",
        status.HTTP_503_SERVICE_UNAVAILABLE: "service_unavailable",
    }
    message_by_status = {
        status.HTTP_404_NOT_FOUND: "Ressource introuvable.",
        status.HTTP_405_METHOD_NOT_ALLOWED: "Méthode non autorisée.",
        status.HTTP_413_CONTENT_TOO_LARGE: "Requête trop volumineuse.",
        status.HTTP_429_TOO_MANY_REQUESTS: "Trop de requêtes, réessayez plus tard.",
        status.HTTP_503_SERVICE_UNAVAILABLE: "Service temporairement indisponible.",
    }
    code = code_by_status.get(exc.status_code, "request_rejected")
    message = message_by_status.get(exc.status_code, "Requête refusée.")
    return _json_error(exc.status_code, code, message)


async def unhandled_exception_handler(
    _request: Request, exc: Exception
) -> JSONResponse:
    logger.exception("Erreur non gérée dans l'API", exc_info=exc)
    return _json_error(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "internal_error",
        "Erreur interne. Réessayez plus tard.",
    )


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApiError, api_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
