"""add gym member profile image

Revision ID: 20260812_000004
Revises: 20260812_000003
Create Date: 2026-08-12 00:40:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260812_000004"
down_revision: Union[str, None] = "20260812_000003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("gym_members", sa.Column("image_url", sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column("gym_members", "image_url")
