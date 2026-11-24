"""Administration : modération des signalements et statistiques réelles."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin, get_db
from app.api.errors import ApiError
from app.core.config import settings
from app.models.analysis import Analysis
from app.models.enums import ReportStatus, RiskLevel
from app.models.report import Report
from app.models.user import User
from app.schemas.admin import (
    AdminReportItem,
    AdminReportListResponse,
    AdminStatsResponse,
    ReviewRequest,
)

router = APIRouter(prefix=settings.api_v1_prefix, tags=["admin"])


@router.get(
    "/admin/reports",
    response_model=AdminReportListResponse,
    operation_id="list_reports_for_review",
)
def list_reports_for_review(
    status_filter: str | None = Query(default=None, alias="status"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    _admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
) -> AdminReportListResponse:
    allowed = {item.value for item in ReportStatus}
    if status_filter is not None and status_filter not in allowed:
        raise ApiError(
            status_code=422,
            code="validation_error",
            message="Statut de filtre invalide.",
        )

    query = select(Report)
    count_query = select(func.count()).select_from(Report)
    if status_filter is not None:
        query = query.where(Report.status == ReportStatus(status_filter))
        count_query = count_query.where(Report.status == ReportStatus(status_filter))

    total = db.scalar(count_query)
    rows = db.scalars(
        query.order_by(Report.created_at.desc()).limit(limit).offset(offset)
    ).all()

    return AdminReportListResponse(
        items=[
            AdminReportItem(
                id=row.id,
                contact_kind=row.contact_kind.value,
                reason_code=row.reason_code,
                status=row.status.value,
                created_at=row.created_at,
                reviewed_at=row.reviewed_at,
            )
            for row in rows
        ],
        total=int(total or 0),
        limit=limit,
        offset=offset,
    )


@router.post(
    "/admin/reports/{report_id}/review",
    response_model=AdminReportItem,
    operation_id="review_report",
)
def review_report(
    report_id: str,
    payload: ReviewRequest,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
) -> AdminReportItem:
    from datetime import datetime, timezone

    report = db.get(Report, report_id)
    if report is None:
        raise ApiError(
            status_code=404, code="not_found", message="Signalement introuvable."
        )

    report.status = ReportStatus(payload.status)
    report.moderator_id = admin.id
    report.reviewed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(report)

    return AdminReportItem(
        id=report.id,
        contact_kind=report.contact_kind.value,
        reason_code=report.reason_code,
        status=report.status.value,
        created_at=report.created_at,
        reviewed_at=report.reviewed_at,
    )


@router.get(
    "/admin/stats",
    response_model=AdminStatsResponse,
    operation_id="admin_stats",
)
def admin_stats(
    _admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
) -> AdminStatsResponse:
    reports = {
        item.value: int(
            db.scalar(
                select(func.count())
                .select_from(Report)
                .where(Report.status == item)
            )
            or 0
        )
        for item in ReportStatus
    }
    analyses = {
        item.value: int(
            db.scalar(
                select(func.count())
                .select_from(Analysis)
                .where(Analysis.risk_level == item)
            )
            or 0
        )
        for item in RiskLevel
    }
    users = int(db.scalar(select(func.count()).select_from(User)) or 0)

    return AdminStatsResponse(
        users=users,
        reports=reports,
        analyses=analyses,
        note=(
            "Statistiques calculées sur la base locale. "
            "Ce ne sont pas des métriques de performance du détecteur."
        ),
    )
