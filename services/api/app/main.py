"""Application FastAPI SAFECLICK."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.errors import register_error_handlers
from app.api.routes import analyze, health, meta, reports
from app.core.config import settings
from app.core.version import API_VERSION

app = FastAPI(
    title="SAFECLICK API",
    version=API_VERSION,
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

register_error_handlers(app)

app.include_router(health.router)
app.include_router(health.v1_router)
app.include_router(meta.router)
app.include_router(reports.router)
app.include_router(analyze.router)


@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    return {
        "name": "SAFECLICK API",
        "version": API_VERSION,
        "docs": "/docs",
        "prefix": settings.api_v1_prefix,
    }
