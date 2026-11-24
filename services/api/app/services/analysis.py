"""Exécute les détecteurs et persiste un résumé non sensible de l'analyse."""

from sqlalchemy.orm import Session

from app.core.hashing import hash_value
from app.detectors import message as message_detector
from app.detectors import url as url_detector
from app.models.analysis import Analysis
from app.models.common import new_id, utcnow
from app.models.enums import AnalysisKind
from app.schemas.analysis import AnalysisResultResponse, IndicatorModel


def _save_and_build(
    db: Session,
    raw: str,
    result: dict[str, object],
    user_id: str | None = None,
) -> AnalysisResultResponse:
    result_id = new_id()
    created_at = utcnow()
    indicators = list(result["indicators"])
    recommendations = list(result["recommendations"])
    limitations = list(result["limitations"])
    level = result["risk_level"]
    score = int(result["score"])
    kind = result["kind"]

    record = Analysis(
        id=result_id,
        user_id=user_id,
        kind=kind,
        input_hash=hash_value(raw, "analysis"),
        input_preview=raw[:255],
        risk_level=level,
        score=score,
        indicators_json=[indicator.to_dict() for indicator in indicators],
        recommendations_json=recommendations,
        limitations_json=limitations,
        engine_version=str(result.get("engine_version", "rules-v1")),
        created_at=created_at,
    )
    db.add(record)
    db.commit()

    return AnalysisResultResponse(
        id=result_id,
        kind=kind,
        risk_level=level,
        score=score,
        indicators=[IndicatorModel(**indicator.to_dict()) for indicator in indicators],
        recommendations=recommendations,
        limitations=limitations,
        created_at=created_at,
    )


def analyze_url(
    db: Session, url: str, user_id: str | None = None
) -> AnalysisResultResponse:
    return _save_and_build(db, url, url_detector.analyze_url(url), user_id)


def analyze_message(
    db: Session, message: str, user_id: str | None = None
) -> AnalysisResultResponse:
    return _save_and_build(db, message, message_detector.analyze_message(message), user_id)


__all__ = ["analyze_message", "analyze_url"]
