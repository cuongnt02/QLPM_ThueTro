"""change type of rating to float

Revision ID: e8e57ced8dde
Revises: 39c215eaf11b
Create Date: 2024-09-20 04:34:22.919318

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e8e57ced8dde'
down_revision = '39c215eaf11b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.alter_column('rating',
               existing_type=mysql.INTEGER(),
               type_=sa.Float(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.alter_column('rating',
               existing_type=sa.Float(),
               type_=mysql.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###
