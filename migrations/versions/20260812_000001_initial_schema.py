"""initial schema

Revision ID: 20260812_000001
Revises: None
Create Date: 2026-08-12 00:00:01
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260812_000001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "permissions",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "roles",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "role_permissions",
        sa.Column("role_id", sa.String(length=64), nullable=False),
        sa.Column("permission_id", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(["permission_id"], ["permissions.id"]),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"]),
        sa.PrimaryKeyConstraint("role_id", "permission_id"),
    )
    op.create_table(
        "internal_users",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("first_name", sa.String(length=80), nullable=False),
        sa.Column("last_name", sa.String(length=80), nullable=False),
        sa.Column("middle_name", sa.String(length=80), nullable=False),
        sa.Column("email", sa.String(length=180), nullable=False),
        sa.Column("phone", sa.String(length=30), nullable=False),
        sa.Column("address", sa.String(length=255), nullable=False),
        sa.Column("role_id", sa.String(length=64), nullable=True),
        sa.Column("role", sa.String(length=80), nullable=True),
        sa.Column("emergency_contacts", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )

    op.create_table(
        "products",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("units", sa.Integer(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "memberships",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("duration", sa.String(length=40), nullable=False),
        sa.Column("includes", sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "promotions",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=150), nullable=False),
        sa.Column("type", sa.String(length=30), nullable=False),
        sa.Column("discount_type", sa.String(length=30), nullable=True),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("start_date", sa.String(length=30), nullable=False),
        sa.Column("end_date", sa.String(length=30), nullable=False),
        sa.Column("code", sa.String(length=60), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("image_url", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )

    op.create_table(
        "gym_members",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("first_name", sa.String(length=80), nullable=False),
        sa.Column("last_name", sa.String(length=80), nullable=False),
        sa.Column("middle_name", sa.String(length=80), nullable=False),
        sa.Column("email", sa.String(length=180), nullable=False),
        sa.Column("phone", sa.String(length=30), nullable=False),
        sa.Column("address", sa.String(length=255), nullable=False),
        sa.Column("birth_date", sa.String(length=30), nullable=True),
        sa.Column("health", sa.JSON(), nullable=True),
        sa.Column("guardian", sa.JSON(), nullable=True),
        sa.Column("emergency_contacts", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("membership_id", sa.String(length=64), nullable=True),
        sa.Column("membership_name", sa.String(length=120), nullable=True),
        sa.ForeignKeyConstraint(["membership_id"], ["memberships.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "member_memberships",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("member_id", sa.String(length=64), nullable=False),
        sa.Column("member_name", sa.String(length=180), nullable=False),
        sa.Column("membership_id", sa.String(length=64), nullable=False),
        sa.Column("membership_name", sa.String(length=120), nullable=False),
        sa.Column("start_date", sa.String(length=30), nullable=False),
        sa.Column("end_date", sa.String(length=30), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(["member_id"], ["gym_members.id"]),
        sa.ForeignKeyConstraint(["membership_id"], ["memberships.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "checkins",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("member_id", sa.String(length=64), nullable=False),
        sa.Column("member_name", sa.String(length=180), nullable=False),
        sa.Column("date", sa.String(length=30), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(["member_id"], ["gym_members.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "development_plans",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("member_id", sa.String(length=64), nullable=False),
        sa.Column("member_name", sa.String(length=180), nullable=False),
        sa.Column("focus", sa.String(length=120), nullable=False),
        sa.Column("coach", sa.String(length=120), nullable=False),
        sa.Column("sessions_per_week", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["member_id"], ["gym_members.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "personal_records",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("member_id", sa.String(length=64), nullable=False),
        sa.Column("member_name", sa.String(length=180), nullable=False),
        sa.Column("category", sa.String(length=20), nullable=False),
        sa.Column("wins", sa.Integer(), nullable=False),
        sa.Column("losses", sa.Integer(), nullable=False),
        sa.Column("draws", sa.Integer(), nullable=False),
        sa.Column("wins_by_ko", sa.Integer(), nullable=False),
        sa.Column("wins_by_points", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["member_id"], ["gym_members.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "sales",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("customer", sa.String(length=180), nullable=False),
        sa.Column("product_id", sa.String(length=64), nullable=False),
        sa.Column("product", sa.String(length=150), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("total", sa.Float(), nullable=False),
        sa.Column("date", sa.String(length=30), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("sales")
    op.drop_table("personal_records")
    op.drop_table("development_plans")
    op.drop_table("checkins")
    op.drop_table("member_memberships")
    op.drop_table("gym_members")
    op.drop_table("promotions")
    op.drop_table("memberships")
    op.drop_table("products")
    op.drop_table("internal_users")
    op.drop_table("role_permissions")
    op.drop_table("roles")
    op.drop_table("permissions")
