"""create sensor_readings table

Revision ID: 009_sensor_readings
Revises: 008_sys_settings
Create Date: 2026-08-24

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "009_sensor_readings"
down_revision: Union[str, None] = "008_sys_settings"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "sensor_readings",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("device_id", sa.String(64), nullable=False),
        sa.Column("topic", sa.String(256), nullable=True),
        sa.Column("reading_type", sa.String(32), nullable=False),
        sa.Column("value_float", sa.Float(), nullable=True),
        sa.Column("value_text", sa.Text(), nullable=True),
        sa.Column("unit", sa.String(16), nullable=True),
        sa.Column("raw_payload", sa.Text(), nullable=True),
        sa.Column("recorded_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_sensor_readings_device_id", "sensor_readings", ["device_id"])
    op.create_index("ix_sensor_readings_reading_type", "sensor_readings", ["reading_type"])
    op.create_index("ix_sensor_readings_recorded_at", "sensor_readings", ["recorded_at"])


def downgrade() -> None:
    op.drop_index("ix_sensor_readings_recorded_at", table_name="sensor_readings")
    op.drop_index("ix_sensor_readings_reading_type", table_name="sensor_readings")
    op.drop_index("ix_sensor_readings_device_id", table_name="sensor_readings")
    op.drop_table("sensor_readings")
