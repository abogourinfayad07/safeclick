"""Contrats d'analyse alignés sur `packages/shared`."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.limits import MESSAGE_MAX_LENGTH, URL_MAX_LENGTH
from app.models.enums import AnalysisKind, RiskLevel


class AnalyzeUrlRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    url: str = Field(min_length=3, max_length=URL_MAX_LENGTH)

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        if any(ord(character) < 32 for character in value):
            raise ValueError("L'URL ne peut pas contenir de caractère de contrôle.")
        if "." not in value:
            raise ValueError("Le domaine est introuvable dans l'URL.")
        return value


class AnalyzeMessageRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    message: str = Field(min_length=5, max_length=MESSAGE_MAX_LENGTH)

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        if any(ord(character) < 32 and character not in "\n\t" for character in value):
            raise ValueError("Le message contient un caractère de contrôle interdit.")
        return value


class IndicatorModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: str
    label: str
    detail: str
    weight: int


class AnalysisResultResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    id: str
    kind: AnalysisKind
    risk_level: RiskLevel = Field(alias="riskLevel")
    score: int = Field(ge=0, le=100)
    indicators: list[IndicatorModel]
    recommendations: list[str]
    limitations: list[str]
    created_at: datetime = Field(alias="createdAt")
