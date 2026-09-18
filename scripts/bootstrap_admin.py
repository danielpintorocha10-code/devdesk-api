"""Cria o primeiro administrador do DevDesk.

Uso: python scripts_bootstrap_admin.py
"""

import getpass

from app.core.database import SessionLocal
from app.core.security import gerar_hash_senha
from app.models.usuario import Usuario


def main() -> None:
    db = SessionLocal()
    try:
        email = input("E-mail do administrador: ").strip().lower()
        nome = input("Nome do administrador: ").strip()
        senha = getpass.getpass("Senha (mínimo 8 caracteres): ")

        if len(senha) < 8:
            raise ValueError("A senha deve possuir pelo menos 8 caracteres.")
        if db.query(Usuario).filter(Usuario.email == email).first():
            raise ValueError("Este e-mail já está cadastrado.")

        admin = Usuario(
            nome=nome,
            email=email,
            senha_hash=gerar_hash_senha(senha),
            perfil="admin",
            ativo=True,
        )
        db.add(admin)
        db.commit()
        print("Administrador criado com sucesso.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
