"""Historique des analyses : seules les analyses du compte sont visibles."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.config import settings
from app.models.analysis import Analysis
from app.models.user import User
from app.schemas.history import AnalysisHistoryItem, AnalysisHistoryResponse

router = APIRouter(prefix=settings.api_v1_prefix, tags=["history"])


@router.get(
    "/analyses",
    response_model=AnalysisHistoryResponse,
    operation_id="list_analyses",
)
def list_analyses(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AnalysisHistoryResponse:
    total = db.scalar(
        select(func.count()).select_from(Analysis).where(Analysis.user_id == user.id)
    )
    rows = db.scalars(
        select(Analysis)
        .where(Analysis.user_id == user.id)
        .order_by(Analysis.created_at.desc())
        .limit(limit)
        .offset(offset)
    ).all()

    return AnalysisHistoryResponse(
        items=[
            AnalysisHistoryItem(
                id=row.id,
                kind=row.kind,
                risk_level=row.risk_level,
                score=row.score,
                input_preview=row.input_preview,
                engine_version=row.engine_version,
                created_at=row.created_at,
            )
            for row in rows
        ],
        total=int(total or 0),
        limit=limit,
        offset=offset,
    )
