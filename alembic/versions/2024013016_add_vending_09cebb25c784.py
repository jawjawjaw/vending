"""add-vending

Revision ID: 09cebb25c784
Revises: e2268d50bdc4
Create Date: 2024-01-30 15:16:55.242303

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "09cebb25c784"
down_revision = "e2268d50bdc4"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("products", sa.Column("vending_id", sa.UUID(), nullable=True))
    op.create_foreign_key(None, "products", "vending_machines", ["vending_id"], ["id"])
    op.add_column("users", sa.Column("vending_id", sa.UUID(), nullable=True))
    op.create_foreign_key(None, "users", "vending_machines", ["vending_id"], ["id"])
    op.create_unique_constraint(None, "vending_machines", ["id"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "vending_machines", type_="unique")
    op.drop_constraint(None, "users", type_="foreignkey")
    op.drop_column("users", "vending_id")
    op.drop_constraint(None, "products", type_="foreignkey")
    op.drop_column("products", "vending_id")
    # ### end Alembic commands ###