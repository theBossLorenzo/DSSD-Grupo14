"""empty message

Revision ID: b82eefec2b76
Revises: c21efe1fc6f1
Create Date: 2021-11-09 14:47:50.416610

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b82eefec2b76'
down_revision = 'c21efe1fc6f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sociedad', sa.Column('qr', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sociedad', 'qr')
    # ### end Alembic commands ###
