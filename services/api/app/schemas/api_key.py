"""Contrats de gestion des clés API : la clé brute n'apparaît qu'à la création."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ApiKeyCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=2, max_length=80)


class ApiKeyCreated(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    id: str
    name: str
    prefix: str
    key: str
    daily_quota: int = Field(alias="dailyQuota")
    created_at: datetime = Field(alias="createdAt")
    notice: str


class ApiKeyItem(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    id: str
    name: str
    prefix: str
    daily_quota: int = Field(alias="dailyQuota")
    usage_count: int = Field(alias="usageCount")
    created_at: datetime = Field(alias="createdAt")
    revoked_at: datetime | None = Field(alias="revokedAt", default=None)


class ApiKeyList(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[ApiKeyItem]
