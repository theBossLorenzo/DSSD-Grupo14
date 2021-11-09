"""empty message

Revision ID: 396fff6af5e2
Revises: acbe3e11af58
Create Date: 2021-11-09 18:14:19.666225

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '396fff6af5e2'
down_revision = 'acbe3e11af58'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sociedad', sa.Column('drive', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sociedad', 'drive')
    # ### end Alembic commands ###
