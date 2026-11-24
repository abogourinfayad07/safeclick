"""Contrat de réponse du endpoint de santé."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    database: str
    environment: str
    version: str
