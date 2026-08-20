"""add auto-capture fields to devices

Revision ID: 003_auto_capture
Revises: 002_devices
Create Date: 2026-08-19

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "003_auto_capture"
down_revision: Union[str, None] = "002_devices"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("devices", sa.Column("auto_capture_enabled", sa.Boolean(), nullable=False, server_default="0"))
    op.add_column("devices", sa.Column("auto_capture_interval_minutes", sa.Integer(), nullable=False, server_default="60"))
    op.add_column("devices", sa.Column("last_auto_capture_at", sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column("devices", "last_auto_capture_at")
    op.drop_column("devices", "auto_capture_interval_minutes")
    op.drop_column("devices", "auto_capture_enabled")
