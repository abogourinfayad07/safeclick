"""En-têtes de sécurité, journalisation sans données sensibles et limitation d'abus."""

from __future__ import annotations

import logging
import time

from fastapi import FastAPI, Request
from starlette.responses import Response

from app.api.errors import json_error
from app.core.config import settings
from app.core.rate_limit import client_ip, is_allowed, route_group

request_logger = logging.getLogger("safeclick.request")


def register_middlewares(app: FastAPI) -> None:
    @app.middleware("http")
    async def security_and_logging(request: Request, call_next):  # type: ignore[no-untyped-def]
        started = time.perf_counter()
        path = request.url.path

        group = route_group(path)
        if group is not None and settings.rate_limit_enabled:
            allowed, retry_after = is_allowed((client_ip(request), group), time.monotonic())
            if not allowed:
                response = json_error(
                    status_code=429,
                    code="rate_limited",
                    message="Trop de requêtes, réessayez plus tard.",
                )
                response.headers["Retry-After"] = str(retry_after)
                request_logger.warning(
                    "Requête refusée par la limitation: %s %s (groupe %s)",
                    request.method,
                    path,
                    group,
                )
                return response

        response: Response = await call_next(request)
        duration_ms = int((time.perf_counter() - started) * 1000)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["Cache-Control"] = "no-store"
        if not settings.is_development:
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )

        # Ni corps, ni en-têtes, ni chaîne de requête : aucun secret dans les logs.
        request_logger.info(
            "%s %s -> %s (%d ms)", request.method, path, response.status_code, duration_ms
        )
        return response
