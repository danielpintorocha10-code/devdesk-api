from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from pwdlib import PasswordHash

from app.core.config import SECRET_KEY


ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


password_hash = PasswordHash.recommended()


def gerar_hash_senha(senha: str) -> str:
    return password_hash.hash(senha)


def verificar_senha(
    senha: str,
    senha_hash: str,
) -> bool:
    return password_hash.verify(
        senha,
        senha_hash,
    )


def criar_access_token(
    dados: dict,
    expires_delta: timedelta | None = None,
) -> str:

    dados_para_token = dados.copy()

    if expires_delta:
        expiracao = (
            datetime.now(timezone.utc)
            + expires_delta
        )
    else:
        expiracao = (
            datetime.now(timezone.utc)
            + timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
        )

    dados_para_token.update(
        {
            "exp": expiracao,
        }
    )

    token = jwt.encode(
        dados_para_token,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return token


def decodificar_token(
    token: str,
) -> dict | None:

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        return payload

    except JWTError:
        return None