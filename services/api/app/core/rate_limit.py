"""Limitation d'abus en mémoire, sans dépendance Redis.

La clé associe l'adresse client et un groupe de routes. Les endpoints de santé
et d'information ne sont pas comptés afin de ne pas bloquer les sondes.
"""

from __future__ import annotations

import threading
import time
from collections import defaultdict, deque

from fastapi import Request

from app.core.config import settings

_PROTECTED_GROUPS = ("/auth", "/analyze", "/reports", "/admin")

_buckets: dict[tuple[str, str], deque[float]] = defaultdict(deque)
_lock = threading.Lock()


def reset_rate_limiter() -> None:
    """Vide l'état en mémoire (tests, redémarrage de worker)."""
    with _lock:
        _buckets.clear()


def route_group(path: str) -> str | None:
    prefix = settings.api_v1_prefix.rstrip("/")
    for group in _PROTECTED_GROUPS:
        if path.startswith(f"{prefix}{group}"):
            return group
    return None


def client_ip(request: Request) -> str:
    return request.client.host if request.client else "unknown"


def is_allowed(key: tuple[str, str], now: float) -> tuple[bool, int]:
    """Fenêtre glissante d'une minute. Renvoie (autorisé, secondes restantes)."""
    window = 60.0
    limit = settings.rate_limit_per_minute
    with _lock:
        bucket = _buckets[key]
        while bucket and bucket[0] <= now - window:
            bucket.popleft()
        if len(bucket) < limit:
            bucket.append(now)
            return True, 0
        retry_after = max(1, int(window - (now - bucket[0])))
        return False, retry_after
