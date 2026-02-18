"""make development plan member assignment optional

Revision ID: 20260812_000005
Revises: 20260812_000004
Create Date: 2026-08-12 01:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260812_000005"
down_revision: Union[str, None] = "20260812_000004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("development_plans", "member_id", existing_type=sa.String(length=64), nullable=True)
    op.alter_column("development_plans", "member_name", existing_type=sa.String(length=180), nullable=True)


def downgrade() -> None:
    op.alter_column("development_plans", "member_name", existing_type=sa.String(length=180), nullable=False)
    op.alter_column("development_plans", "member_id", existing_type=sa.String(length=64), nullable=False)
