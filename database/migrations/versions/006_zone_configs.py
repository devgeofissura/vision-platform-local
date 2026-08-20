"""create zone_configs table

Revision ID: 006_zone_configs
Revises: 005_tracking_sessions
Create Date: 2026-08-20

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "006_zone_configs"
down_revision: Union[str, None] = "005_tracking_sessions"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "zone_configs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("device_id", sa.String(64), nullable=False),
        sa.Column("zone_name", sa.String(64), nullable=False),
        sa.Column("zone_type", sa.String(32), nullable=False),
        sa.Column("polygon_vertices", sa.JSON(), nullable=False),
        sa.Column("zone_config", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("idx_zc_device", "zone_configs", ["device_id"])


def downgrade() -> None:
    op.drop_index("idx_zc_device", table_name="zone_configs")
    op.drop_table("zone_configs")
