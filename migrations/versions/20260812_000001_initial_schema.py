"""initial schema

Revision ID: 20260812_000001
Revises: None
Create Date: 2026-08-12 00:00:01

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "20260812_000001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "catalog_memberships",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("duration_days", sa.Integer(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "inventory_items",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("sku", sa.String(length=80), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("price", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("sku"),
    )

    op.create_table(
        "permissions",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )

    op.create_table(
        "plans",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("price", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "promotions",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("discount_percent", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "roles",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "gym_members",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("full_name", sa.String(length=180), nullable=False),
        sa.Column("email", sa.String(length=180), nullable=True),
        sa.Column("phone", sa.String(length=30), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "internal_users",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("email", sa.String(length=180), nullable=False),
        sa.Column("full_name", sa.String(length=180), nullable=False),
        sa.Column("role_id", sa.String(length=64), nullable=True),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )

    op.create_table(
        "personal_records",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("employee_id", sa.String(length=64), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "gym_memberships",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("member_id", sa.String(length=64), nullable=False),
        sa.Column("plan_id", sa.String(length=64), nullable=False),
        sa.Column("start_date", sa.DateTime(timezone=False), nullable=False),
        sa.Column("end_date", sa.DateTime(timezone=False), nullable=False),
        sa.ForeignKeyConstraint(["member_id"], ["gym_members.id"]),
        sa.ForeignKeyConstraint(["plan_id"], ["plans.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "qr_entries",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("member_id", sa.String(length=64), nullable=False),
        sa.Column("scanned_at", sa.DateTime(timezone=False), nullable=False),
        sa.ForeignKeyConstraint(["member_id"], ["gym_members.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "sales",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("member_id", sa.String(length=64), nullable=True),
        sa.Column("total", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=False), nullable=False),
        sa.ForeignKeyConstraint(["member_id"], ["gym_members.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("sales")
    op.drop_table("qr_entries")
    op.drop_table("gym_memberships")
    op.drop_table("personal_records")
    op.drop_table("internal_users")
    op.drop_table("gym_members")
    op.drop_table("roles")
    op.drop_table("promotions")
    op.drop_table("plans")
    op.drop_table("permissions")
    op.drop_table("inventory_items")
    op.drop_table("catalog_memberships")
