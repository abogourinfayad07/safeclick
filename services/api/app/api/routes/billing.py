"""Offres publiques et abonnement réel de l'utilisateur (sans paiement actif)."""

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.core.config import settings
from app.core.plans import plan_by_code, plans_catalog
from app.models.user import User
from app.schemas.billing import PlansResponse, SubscriptionResponse

router = APIRouter(prefix=settings.api_v1_prefix, tags=["billing"])

_PAYMENT_NOTE = "Aucun paiement n'est actif : les offres PRO et BUSINESS sont sur devis."


@router.get("/billing/plans", response_model=PlansResponse, operation_id="list_plans")
def list_plans() -> PlansResponse:
    return PlansResponse(**plans_catalog())


@router.get(
    "/billing/subscription",
    response_model=SubscriptionResponse,
    operation_id="get_subscription",
)
def get_subscription(user: User = Depends(get_current_user)) -> SubscriptionResponse:
    plan = plan_by_code(user.plan) or plan_by_code("free")
    assert plan is not None
    return SubscriptionResponse(
        plan=user.plan,
        plan_name=str(plan["name"]),
        payment_active=False,
        note=_PAYMENT_NOTE,
    )
