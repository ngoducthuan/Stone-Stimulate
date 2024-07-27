"""Add rating to Product

Revision ID: b563a6f4366e
Revises: 69883961cdbf
Create Date: 2024-07-27 03:21:40.294159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b563a6f4366e'
down_revision = '69883961cdbf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rating', sa.Float(), nullable=False, server_default='0.0'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('rating')

    # ### end Alembic commands ###