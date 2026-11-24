"""Routes d'analyse : validation stricte puis détection passive."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.config import settings
from app.schemas.analysis import (
    AnalyzeMessageRequest,
    AnalyzeUrlRequest,
    AnalysisResultResponse,
)
from app.services.analysis import analyze_message, analyze_url

router = APIRouter(prefix=settings.api_v1_prefix, tags=["analysis"])


@router.post(
    "/analyze/url",
    response_model=AnalysisResultResponse,
    status_code=status.HTTP_200_OK,
    operation_id="analyze_url",
)
def analyze_url_route(
    payload: AnalyzeUrlRequest, db: Session = Depends(get_db)
) -> AnalysisResultResponse:
    return analyze_url(db, payload.url)


@router.post(
    "/analyze/message",
    response_model=AnalysisResultResponse,
    status_code=status.HTTP_200_OK,
    operation_id="analyze_message",
)
def analyze_message_route(
    payload: AnalyzeMessageRequest, db: Session = Depends(get_db)
) -> AnalysisResultResponse:
    return analyze_message(db, payload.message)
