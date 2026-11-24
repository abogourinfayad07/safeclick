"""Énumérations métier, alignées sur les chaînes de `packages/shared`."""

from enum import StrEnum


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class AnalysisKind(StrEnum):
    URL = "url"
    MESSAGE = "message"


class ReportContactKind(StrEnum):
    EMAIL = "email"
    PHONE = "phone"
    URL = "url"
    OTHER = "other"


class ReportStatus(StrEnum):
    UNVERIFIED = "unverified"
    CONFIRMED = "confirmed"
    DISMISSED = "dismissed"
