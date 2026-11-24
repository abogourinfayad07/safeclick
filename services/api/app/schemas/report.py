"""Contrats de signalement : validation stricte et aucune accusation automatique."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator

from app.core.hashing import normalize_contact
from app.core.limits import URL_MAX_LENGTH
from app.models.enums import ReportStatus

ContactKind = Literal["email", "phone", "url", "other"]
ReasonCode = Literal[
    "urgency",
    "payment_request",
    "code_request",
    "impersonation",
    "other",
]


class ReportCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    contact_kind: ContactKind
    contact: str = Field(min_length=3, max_length=URL_MAX_LENGTH)
    reason_code: ReasonCode
    acknowledge_unverified: Literal[True] = Field(
        description="L'utilisateur comprend qu'un signalement n'est pas une preuve."
    )

    @field_validator("contact")
    @classmethod
    def validate_contact(cls, value: str, info: ValidationInfo) -> str:
        if any(ord(character) < 32 for character in value):
            raise ValueError("Le contact ne peut pas contenir de caractère de contrôle.")

        kind = info.data.get("contact_kind")
        normalized = normalize_contact(value, str(kind))

        if len(normalized) < 3:
            raise ValueError("Contact trop court après normalisation.")
        if kind == "email" and normalized.count("@") != 1:
            raise ValueError("Adresse e-mail invalide.")
        if kind == "phone" and len(normalized.lstrip("+")) < 6:
            raise ValueError("Numéro de téléphone trop court.")

        return value


class ReportCreatedResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    status: ReportStatus
    created_at: datetime
    message: str
    disclaimer: str
