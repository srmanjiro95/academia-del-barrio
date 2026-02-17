"""add member qr and membership detail fields

Revision ID: 20260812_000003
Revises: 20260812_000002
Create Date: 2026-08-12 00:20:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260812_000003"
down_revision: Union[str, None] = "20260812_000002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("gym_members", sa.Column("membership_start_date", sa.String(length=30), nullable=True))
    op.add_column("gym_members", sa.Column("membership_end_date", sa.String(length=30), nullable=True))
    op.add_column("gym_members", sa.Column("membership_price", sa.Float(), nullable=True))
    op.add_column("gym_members", sa.Column("qr_uuid", sa.String(length=64), nullable=True))
    op.add_column("gym_members", sa.Column("qr_image_url", sa.String(length=255), nullable=True))
    op.create_unique_constraint("uq_gym_members_qr_uuid", "gym_members", ["qr_uuid"])


def downgrade() -> None:
    op.drop_constraint("uq_gym_members_qr_uuid", "gym_members", type_="unique")
    op.drop_column("gym_members", "qr_image_url")
    op.drop_column("gym_members", "qr_uuid")
    op.drop_column("gym_members", "membership_price")
    op.drop_column("gym_members", "membership_end_date")
    op.drop_column("gym_members", "membership_start_date")
