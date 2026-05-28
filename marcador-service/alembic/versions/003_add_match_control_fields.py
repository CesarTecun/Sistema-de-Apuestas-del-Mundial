"""Add match control fields to partido

Revision ID: 003
Revises: 002
Create Date: 2026-05-21

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add match control fields to partido table
    op.add_column('partido', sa.Column('minuto_actual', sa.Integer(), nullable=True))
    op.add_column('partido', sa.Column('periodo_actual', sa.String(length=20), nullable=True))
    op.add_column('partido', sa.Column('tiempo_extra_periodo', sa.Integer(), nullable=True))
    op.add_column('partido', sa.Column('partido_iniciado', sa.Boolean(), nullable=True))
    op.add_column('partido', sa.Column('partido_pausado', sa.Boolean(), nullable=True))
    op.add_column('partido', sa.Column('faltas_local', sa.Integer(), nullable=True))
    op.add_column('partido', sa.Column('faltas_visitante', sa.Integer(), nullable=True))
    
    # Set default values for existing rows
    op.execute("UPDATE partido SET minuto_actual = 0 WHERE minuto_actual IS NULL")
    op.execute("UPDATE partido SET periodo_actual = '1T' WHERE periodo_actual IS NULL")
    op.execute("UPDATE partido SET tiempo_extra_periodo = 0 WHERE tiempo_extra_periodo IS NULL")
    op.execute("UPDATE partido SET partido_iniciado = FALSE WHERE partido_iniciado IS NULL")
    op.execute("UPDATE partido SET partido_pausado = FALSE WHERE partido_pausado IS NULL")
    op.execute("UPDATE partido SET faltas_local = 0 WHERE faltas_local IS NULL")
    op.execute("UPDATE partido SET faltas_visitante = 0 WHERE faltas_visitante IS NULL")


def downgrade() -> None:
    # Remove match control fields from partido table
    op.drop_column('partido', 'faltas_visitante')
    op.drop_column('partido', 'faltas_local')
    op.drop_column('partido', 'partido_pausado')
    op.drop_column('partido', 'partido_iniciado')
    op.drop_column('partido', 'tiempo_extra_periodo')
    op.drop_column('partido', 'periodo_actual')
    op.drop_column('partido', 'minuto_actual')
