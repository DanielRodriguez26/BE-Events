"""Create eventes table

Revision ID: f2b49927d637
Revises: 
Create Date: 2025-08-20 12:57:54.573772

"""
from alembic import op
import sqlalchemy as sa


# identificadores de revisión, utilizados por Alembic.
revision = 'f2b49927d637'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### comandos generados automáticamente por Alembic - ¡por favor ajusta! ###
    op.create_table('eventes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('location', sa.String(length=255), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_eventes_id'), 'eventes', ['id'], unique=False)
    # ### fin de comandos de Alembic ###


def downgrade() -> None:
    # ### comandos generados automáticamente por Alembic - ¡por favor ajusta! ###
    op.drop_index(op.f('ix_eventes_id'), table_name='eventes')
    op.drop_table('eventes')
    # ### fin de comandos de Alembic ###
