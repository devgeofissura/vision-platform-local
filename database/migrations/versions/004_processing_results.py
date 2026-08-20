"""create processing_results table

Revision ID: 004_processing_results
Revises: 003_auto_capture
Create Date: 2026-08-20

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "004_processing_results"
down_revision: Union[str, None] = "003_auto_capture"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "processing_results",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("observation_id", sa.String(128), sa.ForeignKey("observations.observation_id"), nullable=False),
        sa.Column("device_id", sa.String(64), nullable=False),
        sa.Column("result_type", sa.String(32), nullable=False),
        sa.Column("model_name", sa.String(64), nullable=False),
        sa.Column("model_version", sa.String(32), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("result_data", sa.JSON(), nullable=False),
        sa.Column("inference_ms", sa.Integer(), nullable=True),
        sa.Column("image_width", sa.Integer(), nullable=True),
        sa.Column("image_height", sa.Integer(), nullable=True),
        sa.Column("delivered_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("idx_pr_observation", "processing_results", ["observation_id"])
    op.create_index("idx_pr_device", "processing_results", ["device_id"])
    op.create_index("idx_pr_type", "processing_results", ["result_type"])
    op.create_index("idx_pr_created", "processing_results", ["created_at"])


def downgrade() -> None:
    op.drop_index("idx_pr_created", table_name="processing_results")
    op.drop_index("idx_pr_type", table_name="processing_results")
    op.drop_index("idx_pr_device", table_name="processing_results")
    op.drop_index("idx_pr_observation", table_name="processing_results")
    op.drop_table("processing_results")
