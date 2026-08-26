"""create crack_installations and crack_references tables

Revision ID: 010_crack_installations
Revises: 009_sensor_readings
Create Date: 2026-08-26

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "010_crack_installations"
down_revision: Union[str, None] = "009_sensor_readings"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "crack_installations",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("installation_id", sa.String(64), nullable=False),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("location", sa.String(256), nullable=True),
        sa.Column("camera_id", sa.String(64), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_crack_installations_installation_id", "crack_installations", ["installation_id"], unique=True)
    op.create_index("ix_crack_installations_camera_id", "crack_installations", ["camera_id"])

    op.create_table(
        "crack_references",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("reference_id", sa.String(64), nullable=False),
        sa.Column("installation_id", sa.String(64), sa.ForeignKey("crack_installations.installation_id"), nullable=False),
        sa.Column("image_observation_id", sa.String(128), sa.ForeignKey("observations.observation_id"), nullable=False),
        sa.Column("label_corners", sa.JSON(), nullable=True),
        sa.Column("homography", sa.JSON(), nullable=True),
        sa.Column("marker_points", sa.JSON(), nullable=True),
        sa.Column("line_AB", sa.JSON(), nullable=True),
        sa.Column("line_CD", sa.JSON(), nullable=True),
        sa.Column("intersection", sa.JSON(), nullable=True),
        sa.Column("crack_geometry", sa.JSON(), nullable=True),
        sa.Column("distances", sa.JSON(), nullable=True),
        sa.Column("angles", sa.JSON(), nullable=True),
        sa.Column("quality_score", sa.Float(), nullable=True),
        sa.Column("processing_version", sa.String(32), nullable=False, server_default="1.0.0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_crack_references_reference_id", "crack_references", ["reference_id"], unique=True)
    op.create_index("ix_crack_references_installation_id", "crack_references", ["installation_id"])
    op.create_index("ix_crack_references_image_observation_id", "crack_references", ["image_observation_id"])


def downgrade() -> None:
    op.drop_index("ix_crack_references_image_observation_id", table_name="crack_references")
    op.drop_index("ix_crack_references_installation_id", table_name="crack_references")
    op.drop_index("ix_crack_references_reference_id", table_name="crack_references")
    op.drop_table("crack_references")
    op.drop_index("ix_crack_installations_camera_id", table_name="crack_installations")
    op.drop_index("ix_crack_installations_installation_id", table_name="crack_installations")
    op.drop_table("crack_installations")
