"""Esquema inicial seleccion y partido

Revision ID: 001
Revises:
Create Date: 2026-05-19

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "seleccion",
        sa.Column("id_seleccion", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("pais", sa.String(length=100), nullable=False),
        sa.Column("bandera", sa.String(length=255), nullable=True),
        sa.Column("fk_id_fase_inicial", sa.Integer(), nullable=True),
        sa.Column("status", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id_seleccion"),
    )
    op.create_table(
        "partido",
        sa.Column("id_partido", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("horario", sa.DateTime(timezone=True), nullable=False),
        sa.Column("equipo_local", sa.Integer(), nullable=False),
        sa.Column("equipo_visitante", sa.Integer(), nullable=False),
        sa.Column("fk_sede", sa.Integer(), nullable=True),
        sa.Column("fk_id_fase", sa.Integer(), nullable=True),
        sa.Column("fk_id_liga", sa.Integer(), nullable=True),
        sa.Column("gol_local", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("gol_visitante", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("ganador_penales", sa.Integer(), nullable=True),
        sa.Column("tipo_partido", sa.String(length=50), nullable=False, server_default="Regular"),
        sa.Column("resultado", sa.String(length=50), nullable=True),
        sa.Column("estado", sa.String(length=20), nullable=False, server_default="programado"),
        sa.Column("status", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id_partido"),
    )
    op.create_index("ix_partido_fk_id_liga", "partido", ["fk_id_liga"])


def downgrade() -> None:
    op.drop_index("ix_partido_fk_id_liga", table_name="partido")
    op.drop_table("partido")
    op.drop_table("seleccion")
