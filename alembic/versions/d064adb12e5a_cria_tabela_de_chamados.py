"""cria tabela de chamados

Revision ID: d064adb12e5a
Revises:
Create Date: 2026-09-16 11:18:30.633736
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "d064adb12e5a"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "chamados",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("titulo", sa.String(length=150), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=False),
        sa.Column("prioridade", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("chamados")
