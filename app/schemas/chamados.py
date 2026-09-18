from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Prioridade = Literal["baixa", "media", "alta", "critica"]
StatusChamado = Literal["aberto", "em_andamento", "resolvido", "fechado"]


class ChamadoCreate(BaseModel):
    titulo: str = Field(min_length=3, max_length=150)
    descricao: str = Field(min_length=5)
    prioridade: Prioridade = "media"


class ChamadoAtualizar(BaseModel):
    titulo: str = Field(min_length=3, max_length=150)
    descricao: str = Field(min_length=5)
    prioridade: Prioridade


class ChamadoStatusAtualizar(BaseModel):
    status: StatusChamado


class ChamadoTecnicoAtualizar(BaseModel):
    tecnico_id: int = Field(gt=0)


class ChamadoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    descricao: str
    prioridade: str
    status: str
    usuario_id: int | None
    tecnico_id: int | None
    criado_em: datetime
    atualizado_em: datetime
