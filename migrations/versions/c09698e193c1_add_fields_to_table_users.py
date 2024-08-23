"""add fields to table users

Revision ID: c09698e193c1
Revises: 8bfc401ee793
Create Date: 2024-08-07 19:35:44.925859

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c09698e193c1'
down_revision = '8bfc401ee793'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avatar', sa.String(length=256), nullable=True))
        batch_op.add_column(sa.Column('user_role', sa.Enum('USER', 'ADMIN', 'LANDLORD', name='userrole'), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('user_role')
        batch_op.drop_column('avatar')

    # ### end Alembic commands ###
