"""Schéma initial : users, analyses, reports.

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-11-24
"""

import sqlalchemy as sa
from alembic import op

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


analysis_kind = sa.Enum("url", "message", name="analysis_kind")
risk_level = sa.Enum("low", "medium", "high", name="risk_level")
report_contact_kind = sa.Enum("email", "phone", "url", "other", name="report_contact_kind")
report_status = sa.Enum("unverified", "confirmed", "dismissed", name="report_status")


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.Column("token_version", sa.Integer(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_role", "users", ["role"], unique=False)

    op.create_table(
        "analyses",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column(
            "user_id",
            sa.String(length=36),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("kind", analysis_kind, nullable=False),
        sa.Column("input_hash", sa.String(length=64), nullable=False),
        sa.Column("input_preview", sa.String(length=255), nullable=True),
        sa.Column("risk_level", risk_level, nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("indicators_json", sa.JSON(), nullable=False),
        sa.Column("recommendations_json", sa.JSON(), nullable=False),
        sa.Column("limitations_json", sa.JSON(), nullable=False),
        sa.Column("engine_version", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "score >= 0 AND score <= 100", name="ck_analyses_score"
        ),
    )
    op.create_index("ix_analyses_user_id", "analyses", ["user_id"], unique=False)
    op.create_index("ix_analyses_input_hash", "analyses", ["input_hash"], unique=False)
    op.create_index("ix_analyses_created_at", "analyses", ["created_at"], unique=False)

    op.create_table(
        "reports",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column(
            "reporter_id",
            sa.String(length=36),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("contact_kind", report_contact_kind, nullable=False),
        sa.Column("contact_hash", sa.String(length=64), nullable=False),
        sa.Column("reason_code", sa.String(length=64), nullable=False),
        sa.Column("status", report_status, nullable=False),
        sa.Column(
            "moderator_id",
            sa.String(length=36),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_reports_reporter_id", "reports", ["reporter_id"], unique=False)
    op.create_index("ix_reports_contact_hash", "reports", ["contact_hash"], unique=False)
    op.create_index("ix_reports_reason_code", "reports", ["reason_code"], unique=False)
    op.create_index("ix_reports_status", "reports", ["status"], unique=False)
    op.create_index("ix_reports_moderator_id", "reports", ["moderator_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_reports_moderator_id", table_name="reports")
    op.drop_index("ix_reports_status", table_name="reports")
    op.drop_index("ix_reports_reason_code", table_name="reports")
    op.drop_index("ix_reports_contact_hash", table_name="reports")
    op.drop_index("ix_reports_reporter_id", table_name="reports")
    op.drop_table("reports")

    op.drop_index("ix_analyses_created_at", table_name="analyses")
    op.drop_index("ix_analyses_input_hash", table_name="analyses")
    op.drop_index("ix_analyses_user_id", table_name="analyses")
    op.drop_table("analyses")

    op.drop_index("ix_users_role", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")

    bind = op.get_bind()
    report_status.drop(bind, checkfirst=True)
    report_contact_kind.drop(bind, checkfirst=True)
    risk_level.drop(bind, checkfirst=True)
    analysis_kind.drop(bind, checkfirst=True)
