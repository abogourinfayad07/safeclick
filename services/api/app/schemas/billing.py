"""Contrats publics des offres, sans information de paiement."""

from pydantic import BaseModel, ConfigDict, Field


class PlanModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    code: str
    name: str
    price_label: str = Field(alias="priceLabel")
    daily_analyses: int = Field(alias="dailyAnalyses", gt=0)
    api_keys: int = Field(alias="apiKeys", gt=0)
    description: str
    features: list[str]


class PlansResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    currency: str
    payment_active: bool = Field(alias="paymentActive")
    note: str
    plans: list[PlanModel]


class SubscriptionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    plan: str
    plan_name: str = Field(alias="planName")
    payment_active: bool = Field(alias="paymentActive")
    note: str
