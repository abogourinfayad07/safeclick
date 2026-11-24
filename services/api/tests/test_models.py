"""Contraintes et valeurs par défaut des modèles ORM."""

from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.models import (
    Analysis,
    AnalysisKind,
    Report,
    ReportContactKind,
    ReportStatus,
    RiskLevel,
    User,
)


@pytest.fixture()
def db_session() -> Session:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session
    engine.dispose()


def _user(email: str = "test@example.com") -> User:
    return User(email=email, password_hash="hash-de-test")


def test_user_defaults_and_unique_email(db_session: Session) -> None:
    user = _user()
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id
    assert user.role == "user"
    assert user.token_version == 0
    assert user.is_verified is False
    assert isinstance(user.created_at, datetime)

    db_session.add(_user())
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_analysis_enums_and_score_constraint(db_session: Session) -> None:
    user = _user()
    db_session.add(user)
    db_session.commit()

    analysis = Analysis(
        user_id=user.id,
        kind=AnalysisKind.URL,
        input_hash="a" * 64,
        input_preview="exemple.fr",
        risk_level=RiskLevel.LOW,
        score=12,
    )
    db_session.add(analysis)
    db_session.commit()
    db_session.refresh(analysis)

    assert analysis.engine_version == "rules-v0"
    assert analysis.indicators_json == []
    assert analysis.recommendations_json == []
    assert analysis.limitations_json == []
    assert analysis.input_preview == "exemple.fr"

    db_session.add(
        Analysis(
            kind=AnalysisKind.MESSAGE,
            input_hash="b" * 64,
            risk_level=RiskLevel.HIGH,
            score=101,
        )
    )
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_report_defaults_are_unverified(db_session: Session) -> None:
    report = Report(
        contact_kind=ReportContactKind.PHONE,
        contact_hash="c" * 64,
        reason_code="urgency",
    )
    db_session.add(report)
    db_session.commit()
    db_session.refresh(report)

    assert report.status is ReportStatus.UNVERIFIED
    assert report.reporter_id is None
    assert report.reviewed_at is None
    assert report.moderator_id is None
