"""add image columns

Revision ID: 20260812_000002
Revises: 20260812_000001
Create Date: 2026-08-12 00:10:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260812_000002"
down_revision: Union[str, None] = "20260812_000001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("products", sa.Column("image_url", sa.String(length=255), nullable=True))
    op.add_column("memberships", sa.Column("image_url", sa.String(length=255), nullable=True))
    op.add_column("internal_users", sa.Column("image_url", sa.String(length=255), nullable=True))
    op.add_column("personal_records", sa.Column("image_url", sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column("personal_records", "image_url")
    op.drop_column("internal_users", "image_url")
    op.drop_column("memberships", "image_url")
    op.drop_column("products", "image_url")
