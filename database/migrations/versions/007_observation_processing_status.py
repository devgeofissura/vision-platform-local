"""add processing_status columns to observations

Revision ID: 007_observation_processing_status
Revises: 006_zone_configs
Create Date: 2026-08-20

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "007_observation_processing_status"
down_revision: Union[str, None] = "006_zone_configs"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("observations", sa.Column("processing_status", sa.String(32), nullable=False, server_default="none"))
    op.add_column("observations", sa.Column("processing_started_at", sa.DateTime(), nullable=True))
    op.add_column("observations", sa.Column("processing_completed_at", sa.DateTime(), nullable=True))
    op.create_index("idx_obs_processing_status", "observations", ["processing_status"])


def downgrade() -> None:
    op.drop_index("idx_obs_processing_status", table_name="observations")
    op.drop_column("observations", "processing_completed_at")
    op.drop_column("observations", "processing_started_at")
    op.drop_column("observations", "processing_status")
