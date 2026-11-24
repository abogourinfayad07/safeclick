"""Contrats Pydantic communs à toutes les routes versionnées."""

from pydantic import BaseModel, ConfigDict, Field


class ApiLimits(BaseModel):
    model_config = ConfigDict(extra="forbid")

    url_max_length: int = Field(gt=0)
    message_max_length: int = Field(gt=0)


class ApiInfoResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    version: str
    prefix: str
    supported_languages: list[str]
    analysis_kinds: list[str]
    limits: ApiLimits
    disclaimer: str


class ErrorField(BaseModel):
    model_config = ConfigDict(extra="forbid")

    field: str
    message: str


class ErrorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: str
    message: str
    details: list[ErrorField] | None = None
