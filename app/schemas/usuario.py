from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

Perfil = Literal["usuario", "tecnico", "admin"]


class UsuarioCreate(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    email: EmailStr
    senha: str = Field(min_length=8, max_length=128)


class UsuarioAdminCreate(UsuarioCreate):
    perfil: Perfil


class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: EmailStr
    perfil: str
    ativo: bool
