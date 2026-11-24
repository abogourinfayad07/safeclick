"""Contrats d'administration : modération et statistiques mesurées."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ReviewStatus = Literal["confirmed", "dismissed"]


class AdminReportItem(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    id: str
    contact_kind: str = Field(alias="contactKind")
    reason_code: str = Field(alias="reasonCode")
    status: str
    created_at: datetime = Field(alias="createdAt")
    reviewed_at: datetime | None = Field(alias="reviewedAt", default=None)


class AdminReportListResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[AdminReportItem]
    total: int = Field(ge=0)
    limit: int = Field(ge=1, le=100)
    offset: int = Field(ge=0)


class ReviewRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: ReviewStatus


class AdminStatsResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    users: int = Field(ge=0)
    reports: dict[str, int]
    analyses: dict[str, int]
    note: str
