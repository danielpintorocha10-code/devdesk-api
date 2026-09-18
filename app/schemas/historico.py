from datetime import datetime

from pydantic import BaseModel, ConfigDict


class HistoricoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    chamado_id: int
    usuario_id: int
    acao: str
    descricao: str
    criado_em: datetime