# Checklist para publicar o DevDesk no GitHub

Este guia foi feito para você publicar o projeto de forma profissional sem inventar histórico ou colocar arquivos sensíveis no repositório.

## 1. Criar o repositório

Nome sugerido:

```text
devdesk-api
```

Descrição do repositório:

```text
API REST de Help Desk com FastAPI, PostgreSQL, JWT, RBAC, Alembic, testes automatizados e Docker.
```

Não é necessário adicionar README, `.gitignore` ou licença pelo site do GitHub, porque esses arquivos já estão no projeto.

## 2. Tópicos do repositório

Depois de criar o repositório, adicione estes **Topics** na página do GitHub:

```text
python
fastapi
rest-api
postgresql
sqlalchemy
alembic
jwt
oauth2
pytest
docker
github-actions
backend
backend-development
portfolio
```

## 3. Publicar o projeto

Abra o terminal na pasta raiz do projeto:

```bash
git init
git status
git add .
git commit -m "feat: inicializa DevDesk API"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/devdesk-api.git
git push -u origin main
```

Substitua `SEU-USUARIO` pelo seu usuário do GitHub.

## 4. Conferência antes do push

Rode:

```bash
git status
git ls-files
```

Confirme que **não** aparecem:

```text
.env
.venv/
__pycache__/
*.db
```

Também não publique senhas reais, tokens ou chaves secretas.

## 5. Commits para alterações futuras

Use mensagens curtas e descritivas:

```text
feat: adiciona filtros de chamados
fix: corrige autorização por perfil
test: adiciona testes de autenticação
docs: melhora documentação da API
refactor: reorganiza camada de serviços
```

Não crie commits artificiais apenas para parecer que o projeto teve meses de desenvolvimento. Um histórico pequeno e verdadeiro é melhor para entrevista.

## 6. O que destacar no GitHub

Na descrição e nas conversas técnicas, destaque:

- API REST com FastAPI
- JWT/OAuth2
- RBAC
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker
- Pytest
- GitHub Actions
- Argon2
- Auditoria/histórico
- Regras de autorização por proprietário do recurso

## 7. Como apresentar o projeto em 60 segundos

> "O DevDesk é uma API REST de help desk que desenvolvi com Python e FastAPI. O sistema possui autenticação JWT, três perfis de acesso e regras de autorização por recurso. Usei PostgreSQL com SQLAlchemy e Alembic para persistência e migrations, Pytest para os testes e Docker para padronizar o ambiente. Também implementei comentários e um histórico de auditoria para registrar alterações nos chamados. O projeto possui CI com GitHub Actions e documentação OpenAPI através do Swagger."

## 8. Ordem para mostrar o projeto

1. README
2. Swagger `/docs`
3. `app/routers/`
4. `app/core/security.py`
5. `app/models/`
6. `alembic/versions/`
7. `tests/`
8. `.github/workflows/ci.yml`
9. Docker/Compose

Essa ordem mostra primeiro o resultado e depois as decisões de implementação.
