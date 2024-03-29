"""empty message

Revision ID: 0e5fe68ffb70
Revises: 470e4dfb8e4a
Create Date: 2021-10-19 09:01:36.804511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e5fe68ffb70'
down_revision = '470e4dfb8e4a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('permiso',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=255), nullable=True),
    sa.Column('enabled', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rol_tiene_permiso',
    sa.Column('rol_id', sa.Integer(), nullable=False),
    sa.Column('permiso_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['permiso_id'], ['permiso.id'], ),
    sa.ForeignKeyConstraint(['rol_id'], ['rol.id'], ),
    sa.PrimaryKeyConstraint('rol_id', 'permiso_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rol_tiene_permiso')
    op.drop_table('permiso')
    # ### end Alembic commands ###
