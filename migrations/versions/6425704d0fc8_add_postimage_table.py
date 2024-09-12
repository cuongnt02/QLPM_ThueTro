"""add PostImage table

Revision ID: 6425704d0fc8
Revises: 1bbd7e63ee60
Create Date: 2024-09-06 05:13:13.324523

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6425704d0fc8'
down_revision = '1bbd7e63ee60'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_images',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('image_path', sa.String(length=256), nullable=False),
    sa.Column('post_id', sa.String(length=36), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_images')
    # ### end Alembic commands ###
