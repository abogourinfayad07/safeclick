"""Ajout du plan utilisateur et des clés API.

Revision ID: 0002_billing_api_keys
Revises: 0001_initial_schema
Create Date: 2026-11-24
"""

import sqlalchemy as sa
from alembic import op

revision = "0002_billing_api_keys"
down_revision = "0001_initial_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "plan",
            sa.String(length=16),
            nullable=False,
            server_default="free",
        ),
    )
    op.create_index("ix_users_plan", "users", ["plan"], unique=False)

    op.create_table(
        "api_keys",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column(
            "user_id",
            sa.String(length=36),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("prefix", sa.String(length=16), nullable=False),
        sa.Column("key_hash", sa.String(length=64), nullable=False),
        sa.Column("daily_quota", sa.Integer(), nullable=False),
        sa.Column("usage_date", sa.Date(), nullable=True),
        sa.Column("usage_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("daily_quota > 0", name="ck_api_keys_daily_quota"),
        sa.CheckConstraint("usage_count >= 0", name="ck_api_keys_usage_count"),
    )
    op.create_index("ix_api_keys_user_id", "api_keys", ["user_id"], unique=False)
    op.create_index("ix_api_keys_key_hash", "api_keys", ["key_hash"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_api_keys_key_hash", table_name="api_keys")
    op.drop_index("ix_api_keys_user_id", table_name="api_keys")
    op.drop_table("api_keys")
    op.drop_index("ix_users_plan", table_name="users")
    op.drop_column("users", "plan")
