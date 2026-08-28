"""create fabric_annotations table

Revision ID: 012_fabric_annotations
Revises: 011_crack_reference_nullable
Create Date: 2026-08-28

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "012_fabric_annotations"
down_revision: Union[str, None] = "011_crack_reference_nullable"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "fabric_annotations",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("annotation_id", sa.String(64), nullable=False),
        sa.Column("observation_id", sa.String(128), nullable=True),
        sa.Column("camera_id", sa.String(64), nullable=False),
        sa.Column("defect_type", sa.String(32), nullable=False, server_default="hole"),
        sa.Column("severity", sa.String(16), nullable=True, server_default="low"),
        sa.Column("bbox", sa.JSON(), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("image_width", sa.Integer(), nullable=True),
        sa.Column("image_height", sa.Integer(), nullable=True),
        sa.Column("source", sa.String(16), nullable=True, server_default="classical"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_fabric_annotations_annotation_id", "fabric_annotations", ["annotation_id"], unique=True)
    op.create_index("ix_fabric_annotations_camera_id", "fabric_annotations", ["camera_id"])
    op.create_index("ix_fabric_annotations_observation_id", "fabric_annotations", ["observation_id"])


def downgrade() -> None:
    op.drop_index("ix_fabric_annotations_observation_id", table_name="fabric_annotations")
    op.drop_index("ix_fabric_annotations_camera_id", table_name="fabric_annotations")
    op.drop_index("ix_fabric_annotations_annotation_id", table_name="fabric_annotations")
    op.drop_table("fabric_annotations")
