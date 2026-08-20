"""create tracking_sessions table

Revision ID: 005_tracking_sessions
Revises: 004_processing_results
Create Date: 2026-08-20

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "005_tracking_sessions"
down_revision: Union[str, None] = "004_processing_results"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tracking_sessions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("session_id", sa.String(128), unique=True, nullable=False),
        sa.Column("device_id", sa.String(64), nullable=False),
        sa.Column("entity_type", sa.String(32), nullable=False),
        sa.Column("entity_id", sa.String(64), nullable=True),
        sa.Column("first_seen_at", sa.DateTime(), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(), nullable=False),
        sa.Column("frame_count", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("avg_bbox_width", sa.Float(), nullable=True),
        sa.Column("avg_bbox_height", sa.Float(), nullable=True),
        sa.Column("path_centroids", sa.JSON(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("idx_ts_device", "tracking_sessions", ["device_id"])
    op.create_index("idx_ts_entity", "tracking_sessions", ["entity_type", "entity_id"])
    op.create_index("idx_ts_active", "tracking_sessions", ["is_active"])


def downgrade() -> None:
    op.drop_index("idx_ts_active", table_name="tracking_sessions")
    op.drop_index("idx_ts_entity", table_name="tracking_sessions")
    op.drop_index("idx_ts_device", table_name="tracking_sessions")
    op.drop_table("tracking_sessions")
