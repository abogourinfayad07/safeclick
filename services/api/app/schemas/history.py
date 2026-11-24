"""Historique des analyses de l'utilisateur authentifié."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import AnalysisKind, RiskLevel


class AnalysisHistoryItem(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    id: str
    kind: AnalysisKind
    risk_level: RiskLevel = Field(alias="riskLevel")
    score: int = Field(ge=0, le=100)
    input_preview: str | None = Field(alias="inputPreview", default=None)
    engine_version: str = Field(alias="engineVersion")
    created_at: datetime = Field(alias="createdAt")


class AnalysisHistoryResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[AnalysisHistoryItem]
    total: int = Field(ge=0)
    limit: int = Field(ge=1, le=100)
    offset: int = Field(ge=0)
