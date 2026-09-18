from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ComentarioCreate(BaseModel):
    texto: str = Field(min_length=1, max_length=2000)


class ComentarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    chamado_id: int
    usuario_id: int
    texto: str
    criado_em: datetime
