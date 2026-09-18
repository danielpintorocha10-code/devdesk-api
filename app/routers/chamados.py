from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.chamado import Chamado
from app.models.comentario import Comentario
from app.models.historico import Historico
from app.models.usuario import Usuario
from app.routers.auth import obter_tecnico, obter_usuario_atual
from app.schemas.chamados import (
    ChamadoAtualizar,
    ChamadoCreate,
    ChamadoResponse,
    ChamadoStatusAtualizar,
    ChamadoTecnicoAtualizar,
)
from app.schemas.comentario import ComentarioCreate, ComentarioResponse
from app.schemas.historico import HistoricoResponse

router = APIRouter(prefix="/chamados", tags=["Chamados"])


def buscar_ou_404(chamado_id: int, db: Session) -> Chamado:
    chamado = db.query(Chamado).filter(Chamado.id == chamado_id).first()
    if chamado is None:
        raise HTTPException(status_code=404, detail="Chamado não encontrado.")
    return chamado


def pode_acessar_chamado(chamado: Chamado, usuario: Usuario) -> bool:
    return usuario.perfil in {"tecnico", "admin"} or chamado.usuario_id == usuario.id


def registrar_historico(
    db: Session,
    chamado: Chamado,
    usuario: Usuario,
    acao: str,
    descricao: str,
) -> None:
    db.add(
        Historico(
            chamado_id=chamado.id,
            usuario_id=usuario.id,
            acao=acao,
            descricao=descricao,
        )
    )


@router.post("/", response_model=ChamadoResponse, status_code=status.HTTP_201_CREATED)
def criar_chamado(
    chamado: ChamadoCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual),
):
    novo_chamado = Chamado(
        titulo=chamado.titulo,
        descricao=chamado.descricao,
        prioridade=chamado.prioridade,
        status="aberto",
        usuario_id=usuario.id,
    )
    db.add(novo_chamado)
    db.flush()
    registrar_historico(db, novo_chamado, usuario, "criacao", "Chamado criado.")
    db.commit()
    db.refresh(novo_chamado)
    return novo_chamado


@router.get("/", response_model=list[ChamadoResponse])
def listar_chamados(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual),
):
    query = db.query(Chamado).order_by(Chamado.id.desc())
    if usuario.perfil not in {"tecnico", "admin"}:
        query = query.filter(Chamado.usuario_id == usuario.id)
    return query.all()


@router.get("/{chamado_id}", response_model=ChamadoResponse)
def buscar_chamado(
    chamado_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual),
):
    chamado = buscar_ou_404(chamado_id, db)
    if not pode_acessar_chamado(chamado, usuario):
        raise HTTPException(status_code=403, detail="Você não pode acessar este chamado.")
    return chamado


@router.put("/{chamado_id}", response_model=ChamadoResponse)
def atualizar_chamado(
    chamado_id: int,
    chamado_atualizado: ChamadoAtualizar,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual),
):
    chamado = buscar_ou_404(chamado_id, db)
    if not pode_acessar_chamado(chamado, usuario):
        raise HTTPException(status_code=403, detail="Você não pode alterar este chamado.")

    chamado.titulo = chamado_atualizado.titulo
    chamado.descricao = chamado_atualizado.descricao
    chamado.prioridade = chamado_atualizado.prioridade
    registrar_historico(db, chamado, usuario, "atualizacao", "Dados do chamado atualizados.")
    db.commit()
    db.refresh(chamado)
    return chamado


@router.patch("/{chamado_id}/status", response_model=ChamadoResponse)
def atualizar_status(
    chamado_id: int,
    dados: ChamadoStatusAtualizar,
    db: Session = Depends(get_db),
    tecnico: Usuario = Depends(obter_tecnico),
):
    chamado = buscar_ou_404(chamado_id, db)
    status_anterior = chamado.status
    chamado.status = dados.status
    registrar_historico(
        db,
        chamado,
        tecnico,
        "alteracao_status",
        f"Status alterado de '{status_anterior}' para '{dados.status}'.",
    )
    db.commit()
    db.refresh(chamado)
    return chamado


@router.patch("/{chamado_id}/tecnico", response_model=ChamadoResponse)
def atribuir_tecnico(
    chamado_id: int,
    dados: ChamadoTecnicoAtualizar,
    db: Session = Depends(get_db),
    tecnico_atual: Usuario = Depends(obter_tecnico),
):
    chamado = buscar_ou_404(chamado_id, db)
    tecnico = (
        db.query(Usuario)
        .filter(Usuario.id == dados.tecnico_id, Usuario.ativo.is_(True))
        .first()
    )
    if tecnico is None:
        raise HTTPException(status_code=404, detail="Técnico não encontrado.")
    if tecnico.perfil not in {"tecnico", "admin"}:
        raise HTTPException(status_code=400, detail="O usuário informado não é técnico.")

    chamado.tecnico_id = tecnico.id
    registrar_historico(
        db,
        chamado,
        tecnico_atual,
        "atribuicao_tecnico",
        f"Chamado atribuído ao usuário {tecnico.nome}.",
    )
    db.commit()
    db.refresh(chamado)
    return chamado


@router.post("/{chamado_id}/comentarios", response_model=ComentarioResponse, status_code=201)
def adicionar_comentario(
    chamado_id: int,
    dados: ComentarioCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual),
):
    chamado = buscar_ou_404(chamado_id, db)
    if not pode_acessar_chamado(chamado, usuario):
        raise HTTPException(status_code=403, detail="Você não pode comentar neste chamado.")

    comentario = Comentario(chamado_id=chamado.id, usuario_id=usuario.id, texto=dados.texto)
    db.add(comentario)
    registrar_historico(db, chamado, usuario, "comentario", "Novo comentário adicionado.")
    db.commit()
    db.refresh(comentario)
    return comentario


@router.get("/{chamado_id}/comentarios", response_model=list[ComentarioResponse])
def listar_comentarios(
    chamado_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual),
):
    chamado = buscar_ou_404(chamado_id, db)
    if not pode_acessar_chamado(chamado, usuario):
        raise HTTPException(status_code=403, detail="Você não pode acessar estes comentários.")
    return (
        db.query(Comentario)
        .filter(Comentario.chamado_id == chamado_id)
        .order_by(Comentario.id.asc())
        .all()
    )


@router.get("/{chamado_id}/historico", response_model=list[HistoricoResponse])
def listar_historico(
    chamado_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual),
):
    chamado = buscar_ou_404(chamado_id, db)
    if not pode_acessar_chamado(chamado, usuario):
        raise HTTPException(status_code=403, detail="Você não pode acessar este histórico.")
    return (
        db.query(Historico)
        .filter(Historico.chamado_id == chamado_id)
        .order_by(Historico.id.asc())
        .all()
    )


@router.delete("/{chamado_id}")
def remover_chamado(
    chamado_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual),
):
    chamado = buscar_ou_404(chamado_id, db)
    if usuario.perfil not in {"admin"} and chamado.usuario_id != usuario.id:
        raise HTTPException(status_code=403, detail="Você não pode remover este chamado.")

    db.query(Comentario).filter(Comentario.chamado_id == chamado_id).delete(synchronize_session=False)
    db.query(Historico).filter(Historico.chamado_id == chamado_id).delete(synchronize_session=False)
    db.delete(chamado)
    db.commit()
    return {"mensagem": "Chamado removido com sucesso."}
