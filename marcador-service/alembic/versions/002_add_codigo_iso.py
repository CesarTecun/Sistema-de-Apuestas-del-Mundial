"""add codigo_iso to seleccion

Revision ID: 002
Revises: 001
Create Date: 2026-05-20

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("seleccion", sa.Column("codigo_iso", sa.String(length=3), nullable=True))
    op.create_index("ix_seleccion_codigo_iso", "seleccion", ["codigo_iso"])


def downgrade() -> None:
    op.drop_index("ix_seleccion_codigo_iso", table_name="seleccion")
    op.drop_column("seleccion", "codigo_iso")
