"""adiciona campos de relacionamento aos chamados

Revision ID: b986641d222f
Revises: 5ca9daea488f
Create Date: 2026-09-17 11:09:28.063879
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "b986641d222f"
down_revision: Union[str, Sequence[str], None] = "5ca9daea488f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("chamados", sa.Column("usuario_id", sa.Integer(), nullable=True))
    op.add_column("chamados", sa.Column("tecnico_id", sa.Integer(), nullable=True))
    op.add_column("chamados", sa.Column("criado_em", sa.DateTime(timezone=True), nullable=True))
    op.add_column("chamados", sa.Column("atualizado_em", sa.DateTime(timezone=True), nullable=True))

    op.create_foreign_key(
        "fk_chamados_usuario_id", "chamados", "usuarios", ["usuario_id"], ["id"]
    )
    op.create_foreign_key(
        "fk_chamados_tecnico_id", "chamados", "usuarios", ["tecnico_id"], ["id"]
    )

    op.execute(
        "UPDATE chamados SET criado_em = CURRENT_TIMESTAMP, atualizado_em = CURRENT_TIMESTAMP "
        "WHERE criado_em IS NULL OR atualizado_em IS NULL"
    )
    op.alter_column("chamados", "criado_em", nullable=False)
    op.alter_column("chamados", "atualizado_em", nullable=False)


def downgrade() -> None:
    op.drop_constraint("fk_chamados_tecnico_id", "chamados", type_="foreignkey")
    op.drop_constraint("fk_chamados_usuario_id", "chamados", type_="foreignkey")
    op.drop_column("chamados", "atualizado_em")
    op.drop_column("chamados", "criado_em")
    op.drop_column("chamados", "tecnico_id")
    op.drop_column("chamados", "usuario_id")
