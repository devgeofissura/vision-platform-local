"""add devices table

Revision ID: 002_devices
Revises: 001_initial
Create Date: 2026-08-19

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "002_devices"
down_revision: Union[str, None] = "001_initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "devices",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("device_id", sa.String(64), nullable=False),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("device_type", sa.String(32), nullable=False, server_default="camera"),
        sa.Column("task_type", sa.String(32), nullable=False, server_default="fissure"),
        sa.Column("connection_type", sa.String(32), nullable=False, server_default="rtsp"),
        sa.Column("connection_config", sa.JSON(), nullable=True),
        sa.Column("capture_interval_ms", sa.Integer(), nullable=False, server_default="60000"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_devices_device_id", "devices", ["device_id"], unique=True)


def downgrade() -> None:
    op.drop_table("devices")
