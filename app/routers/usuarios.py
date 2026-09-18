from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import gerar_hash_senha
from app.models.usuario import Usuario
from app.routers.auth import obter_admin
from app.schemas.usuario import UsuarioAdminCreate, UsuarioCreate, UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


def email_existente(db: Session, email: str) -> bool:
    return db.query(Usuario).filter(Usuario.email == email).first() is not None


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if email_existente(db, usuario.email):
        raise HTTPException(status_code=409, detail="E-mail já cadastrado.")

    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=gerar_hash_senha(usuario.senha),
        perfil="usuario",
        ativo=True,
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario


@router.post("/admin", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario_admin(
    usuario: UsuarioAdminCreate,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(obter_admin),
):
    if email_existente(db, usuario.email):
        raise HTTPException(status_code=409, detail="E-mail já cadastrado.")

    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=gerar_hash_senha(usuario.senha),
        perfil=usuario.perfil,
        ativo=True,
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(
    db: Session = Depends(get_db),
    admin: Usuario = Depends(obter_admin),
):
    return db.query(Usuario).order_by(Usuario.id.asc()).all()
