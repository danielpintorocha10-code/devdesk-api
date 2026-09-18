from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    criar_access_token,
    decodificar_token,
    verificar_senha,
)
from app.models.usuario import Usuario
from app.schemas.auth import Token
from app.schemas.usuario import UsuarioResponse

router = APIRouter(prefix="/auth", tags=["Autenticação"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/login", response_model=Token)
def login(
    formulario: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    usuario = db.query(Usuario).filter(Usuario.email == formulario.username).first()
    if usuario is None or not verificar_senha(formulario.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not usuario.ativo:
        raise HTTPException(status_code=403, detail="Usuário inativo.")

    access_token = criar_access_token(
        dados={"sub": str(usuario.id), "perfil": usuario.perfil},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


def obter_usuario_atual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    payload = decodificar_token(token)
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    usuario_id = payload.get("sub")
    try:
        usuario_id = int(usuario_id)
    except (TypeError, ValueError):
        raise HTTPException(status_code=401, detail="Token inválido.") from None

    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=401, detail="Usuário não encontrado.")
    if not usuario.ativo:
        raise HTTPException(status_code=403, detail="Usuário inativo.")
    return usuario


def obter_tecnico(usuario: Usuario = Depends(obter_usuario_atual)) -> Usuario:
    if usuario.perfil not in {"tecnico", "admin"}:
        raise HTTPException(status_code=403, detail="Acesso permitido apenas para técnicos.")
    return usuario


def obter_admin(usuario: Usuario = Depends(obter_usuario_atual)) -> Usuario:
    if usuario.perfil != "admin":
        raise HTTPException(status_code=403, detail="Acesso permitido apenas para administradores.")
    return usuario


@router.get("/me", response_model=UsuarioResponse)
def meu_perfil(usuario: Usuario = Depends(obter_usuario_atual)):
    return usuario


@router.get("/area-tecnica")
def area_tecnica(usuario: Usuario = Depends(obter_tecnico)):
    return {"mensagem": "Acesso autorizado à área técnica.", "usuario": usuario.nome, "perfil": usuario.perfil}


@router.get("/area-admin")
def area_admin(usuario: Usuario = Depends(obter_admin)):
    return {"mensagem": "Acesso autorizado à área administrativa.", "usuario": usuario.nome, "perfil": usuario.perfil}
