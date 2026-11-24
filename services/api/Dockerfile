# Image API SAFECLICK — contexte de build : racine du dépôt.
FROM python:3.15-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/services/api

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 10001 appuser

COPY services/api/requirements.txt ./services/api/requirements.txt
RUN python -m pip install --no-cache-dir -r services/api/requirements.txt

COPY services/api ./services/api
# Le catalogue d'offres est partagé avec le web : il doit être présent dans l'image.
COPY packages/shared/plans.json ./packages/shared/plans.json

RUN mkdir -p /app/data && chown -R appuser:appuser /app

USER appuser
EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "services/api"]
