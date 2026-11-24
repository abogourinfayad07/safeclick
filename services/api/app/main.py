"""Application FastAPI SAFECLICK."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health
from app.core.config import settings

app = FastAPI(
    title="SAFECLICK API",
    version="0.1.0",
    description="API publique de détection des arnaques numériques.",
)

# Le site web et le mobile utilisent la même API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.site_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)


@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    return {
        "name": "SAFECLICK API",
        "version": "0.1.0",
        "docs": "/docs",
        "prefix": settings.api_v1_prefix,
    }
