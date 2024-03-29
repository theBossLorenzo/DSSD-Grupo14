"""empty message

Revision ID: 96b0490cd371
Revises: 9bd7af8441f7
Create Date: 2021-10-20 21:42:48.267160

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96b0490cd371'
down_revision = '9bd7af8441f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sociedad', sa.Column('estatuto_aceptado', sa.Boolean(), nullable=True))
    op.add_column('sociedad', sa.Column('comentarioAL', sa.String(), nullable=True))
    op.drop_column('sociedad', 'nroExpediente')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sociedad', sa.Column('nroExpediente', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('sociedad', 'comentarioAL')
    op.drop_column('sociedad', 'estatuto_aceptado')
    # ### end Alembic commands ###
