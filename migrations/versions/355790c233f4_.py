"""empty message

Revision ID: 355790c233f4
Revises: 82d494d3d2b5
Create Date: 2021-10-13 19:06:02.177455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '355790c233f4'
down_revision = '82d494d3d2b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sociedad', sa.Column('comentario', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sociedad', 'comentario')
    # ### end Alembic commands ###
