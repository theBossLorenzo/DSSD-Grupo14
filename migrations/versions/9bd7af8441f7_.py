"""empty message

Revision ID: 9bd7af8441f7
Revises: 00c4e9c39bb4
Create Date: 2021-10-20 12:48:23.225199

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bd7af8441f7'
down_revision = '00c4e9c39bb4'
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
    op.create_table('rol',
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
    op.add_column('sociedad', sa.Column('nroExpediente', sa.Integer(), nullable=True))
    op.add_column('sociedad', sa.Column('estampillado', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sociedad', 'estampillado')
    op.drop_column('sociedad', 'nroExpediente')
    op.drop_table('rol_tiene_permiso')
    op.drop_table('rol')
    op.drop_table('permiso')
    # ### end Alembic commands ###
