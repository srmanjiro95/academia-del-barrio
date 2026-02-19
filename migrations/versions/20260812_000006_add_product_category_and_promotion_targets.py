"""add product category and promotion target columns

Revision ID: 20260812_000006
Revises: 20260812_000005
Create Date: 2026-08-12 00:06:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20260812_000006"
down_revision = "20260812_000005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("products", sa.Column("category", sa.String(length=120), nullable=True))
    op.execute("UPDATE products SET category = 'General' WHERE category IS NULL")
    op.alter_column("products", "category", nullable=False)

    op.add_column(
        "promotions",
        sa.Column("applies_to", sa.String(length=30), nullable=False, server_default="all_store"),
    )
    op.add_column("promotions", sa.Column("target_category", sa.String(length=120), nullable=True))
    op.add_column(
        "promotions",
        sa.Column("target_product_ids", sa.JSON(), nullable=False, server_default=sa.text("'[]'::json")),
    )
    op.add_column(
        "promotions",
        sa.Column("target_membership_ids", sa.JSON(), nullable=False, server_default=sa.text("'[]'::json")),
    )


def downgrade() -> None:
    op.drop_column("promotions", "target_membership_ids")
    op.drop_column("promotions", "target_product_ids")
    op.drop_column("promotions", "target_category")
    op.drop_column("promotions", "applies_to")
    op.drop_column("products", "category")
