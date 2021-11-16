"""empty message

Revision ID: e818eecf850d
Revises: 396fff6af5e2
Create Date: 2021-11-16 15:20:56.258408

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e818eecf850d'
down_revision = '396fff6af5e2'
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
    op.create_table('sociedad',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(), nullable=True),
    sa.Column('estatuto', sa.String(), nullable=True),
    sa.Column('fecha_creacion', sa.Date(), nullable=True),
    sa.Column('domicilio_legal', sa.String(), nullable=True),
    sa.Column('domicilio_real', sa.String(), nullable=True),
    sa.Column('representante', sa.String(), nullable=True),
    sa.Column('correo', sa.String(), nullable=True),
    sa.Column('aceptada', sa.Boolean(), nullable=True),
    sa.Column('comentario', sa.String(), nullable=True),
    sa.Column('caseId', sa.Integer(), nullable=True),
    sa.Column('estampillado', sa.String(), nullable=True),
    sa.Column('estatuto_aceptado', sa.Boolean(), nullable=True),
    sa.Column('comentarioAL', sa.String(), nullable=True),
    sa.Column('nroExpediente', sa.Integer(), nullable=True),
    sa.Column('qr', sa.Integer(), nullable=True),
    sa.Column('drive', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('socio',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_sociedad', sa.Integer(), nullable=True),
    sa.Column('nombre', sa.String(), nullable=True),
    sa.Column('apellido', sa.String(), nullable=True),
    sa.Column('porcentaje', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('estatuto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('data', sa.LargeBinary(), nullable=True),
    sa.Column('id_sociedad', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_sociedad'], ['sociedad.id'], ),
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
    op.drop_table('estatuto')
    op.drop_table('socio')
    op.drop_table('sociedad')
    op.drop_table('rol')
    op.drop_table('permiso')
    # ### end Alembic commands ###
