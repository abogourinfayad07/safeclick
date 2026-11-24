"""Dépôt d'un signalement : contact haché et statut non vérifié."""

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.config import settings
from app.core.hashing import hash_contact
from app.models.enums import ReportContactKind
from app.models.report import Report
from app.schemas.report import ReportCreate, ReportCreatedResponse

router = APIRouter(prefix=settings.api_v1_prefix, tags=["reports"])

DISCLAIMER = (
    "Signalement non vérifié : aucune accusation n'est faite. "
    "Un risque faible n'est jamais une garantie de sécurité."
)


@router.post(
    "/reports",
    response_model=ReportCreatedResponse,
    status_code=status.HTTP_201_CREATED,
    operation_id="create_report",
)
def create_report(
    payload: ReportCreate, db: Session = Depends(get_db)
) -> ReportCreatedResponse:
    contact_hash = hash_contact(payload.contact, payload.contact_kind)

    existing = db.execute(
        select(Report).where(
            Report.contact_hash == contact_hash,
            Report.reason_code == payload.reason_code,
        )
    ).scalar_one_or_none()

    if existing is not None:
        return ReportCreatedResponse(
            id=existing.id,
            status=existing.status,
            created_at=existing.created_at,
            message="Ce signalement a déjà été enregistré.",
            disclaimer=DISCLAIMER,
        )

    report = Report(
        contact_kind=ReportContactKind(payload.contact_kind),
        contact_hash=contact_hash,
        reason_code=payload.reason_code,
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    return ReportCreatedResponse(
        id=report.id,
        status=report.status,
        created_at=report.created_at,
        message="Signalement enregistré pour vérification.",
        disclaimer=DISCLAIMER,
    )
