"""Contrats d'authentification et de profil."""

import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$")


class RegisterRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=12, max_length=128)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        email = value.casefold()
        if not _EMAIL_RE.fullmatch(email):
            raise ValueError("Adresse e-mail invalide.")
        return email

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not any(character.isalpha() for character in value):
            raise ValueError("Le mot de passe doit contenir une lettre.")
        if not any(character.isdigit() for character in value):
            raise ValueError("Le mot de passe doit contenir un chiffre.")
        return value


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=1, max_length=128)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.casefold()


class VerifyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    token: str = Field(min_length=20, max_length=2048)


class RegisterResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: str
    message: str
    verification_required: bool


class TokenResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserProfile(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    email: str
    role: str
    is_verified: bool = Field(alias="isVerified")
    created_at: datetime = Field(alias="createdAt")
