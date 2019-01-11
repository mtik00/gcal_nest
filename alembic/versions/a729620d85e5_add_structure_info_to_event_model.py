"""add structure info to Event model

Revision ID: a729620d85e5
Revises:
Create Date: 2019-01-10 21:16:07.776692

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a729620d85e5"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("events", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("structure_id", sa.String(), nullable=False, server_default="")
        )
        batch_op.add_column(
            sa.Column("structure_name", sa.String(), nullable=False, server_default="")
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("events", schema=None) as batch_op:
        batch_op.drop_column("structure_name")
        batch_op.drop_column("structure_id")

    # ### end Alembic commands ###
