"""Historique d'analyse. Le contenu brut n'est pas conservé."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import JSON, CheckConstraint, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

from .common import new_id, utcnow
from .enums import AnalysisKind, RiskLevel

if TYPE_CHECKING:
    from .user import User


class Analysis(Base):
    __tablename__ = "analyses"
    __table_args__ = (
        CheckConstraint("score >= 0 AND score <= 100", name="ck_analyses_score"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    user_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    kind: Mapped[AnalysisKind] = mapped_column(
        Enum(AnalysisKind, name="analysis_kind"), nullable=False
    )
    input_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    input_preview: Mapped[str | None] = mapped_column(String(255), nullable=True)
    risk_level: Mapped[RiskLevel] = mapped_column(
        Enum(RiskLevel, name="risk_level"), nullable=False
    )
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    indicators_json: Mapped[list[dict[str, object]]] = mapped_column(
        JSON, nullable=False, default=list
    )
    recommendations_json: Mapped[list[str]] = mapped_column(
        JSON, nullable=False, default=list
    )
    limitations_json: Mapped[list[str]] = mapped_column(
        JSON, nullable=False, default=list
    )
    engine_version: Mapped[str] = mapped_column(
        String(32), nullable=False, default="rules-v0"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utcnow, index=True
    )

    user: Mapped["User | None"] = relationship(back_populates="analyses")
