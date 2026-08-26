"""Make image_observation_id nullable and drop FK constraint.

Revision ID: 011
Revises: 010
Create Date: 2026-08-26
"""

import sqlalchemy as sa
from alembic import op

revision = "011_crack_reference_nullable"
down_revision = "010_crack_installations"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop the FK constraint first
    op.drop_constraint(
        "crack_references_image_observation_id_fkey",
        "crack_references",
        type_="foreignkey",
    )
    # Make column nullable
    op.alter_column(
        "crack_references",
        "image_observation_id",
        existing_type=sa.String(128),
        nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "crack_references",
        "image_observation_id",
        existing_type=sa.String(128),
        nullable=False,
    )
    op.create_foreign_key(
        "crack_references_image_observation_id_fkey",
        "crack_references",
        "observations",
        ["image_observation_id"],
        ["observation_id"],
    )
