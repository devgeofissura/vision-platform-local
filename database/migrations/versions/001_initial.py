"""initial schema

Revision ID: 001_initial
Revises:
Create Date: 2026-08-17

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "observations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("observation_id", sa.String(128), nullable=False),
        sa.Column("camera_id", sa.String(64), nullable=False),
        sa.Column("local_id", sa.String(64), nullable=False),
        sa.Column("captured_at", sa.DateTime(), nullable=False),
        sa.Column("file_path", sa.Text(), nullable=False),
        sa.Column("sha256", sa.String(64), nullable=False),
        sa.Column("width", sa.Integer(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column("quality_score", sa.Float(), nullable=True),
        sa.Column("quality_issues", sa.Text(), nullable=True),
        sa.Column("algorithm_version", sa.String(32), nullable=True),
        sa.Column("delivery_status", sa.String(32), nullable=False, server_default="pending"),
        sa.Column("delivery_attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_delivery_at", sa.DateTime(), nullable=True),
        sa.Column("last_delivery_error", sa.Text(), nullable=True),
        sa.Column("delivered_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_observations_observation_id", "observations", ["observation_id"], unique=True)
    op.create_index("ix_observations_camera_id", "observations", ["camera_id"])
    op.create_index("ix_observations_local_id", "observations", ["local_id"])
    op.create_index("ix_observations_captured_at", "observations", ["captured_at"])
    op.create_index("ix_observations_delivery_status", "observations", ["delivery_status"])

    op.create_table(
        "delivery_logs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("observation_id", sa.String(128), sa.ForeignKey("observations.observation_id"), nullable=False),
        sa.Column("attempt", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("status_code", sa.Integer(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_delivery_logs_observation_id", "delivery_logs", ["observation_id"])


def downgrade() -> None:
    op.drop_table("delivery_logs")
    op.drop_table("observations")
