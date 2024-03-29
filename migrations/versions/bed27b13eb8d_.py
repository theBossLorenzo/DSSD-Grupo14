"""empty message

Revision ID: bed27b13eb8d
Revises: 43d919110a25
Create Date: 2021-11-02 21:45:31.640971

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bed27b13eb8d'
down_revision = '43d919110a25'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('estatuto', sa.Column('id_sociedad', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'estatuto', 'sociedad', ['id_sociedad'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'estatuto', type_='foreignkey')
    op.drop_column('estatuto', 'id_sociedad')
    # ### end Alembic commands ###
