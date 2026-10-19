# DevDesk API

> **API REST de Help Desk desenvolvida com FastAPI, PostgreSQL e JWT, com controle de acesso por perfis, auditoria, testes automatizados e Docker.**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-REST-009688)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED)](https://www.docker.com/)

## Sobre o projeto

O **DevDesk** simula o back-end de uma plataforma de suporte de TI. Usuários podem abrir e acompanhar chamados, enquanto técnicos e administradores possuem permissões adicionais para atuar no atendimento.

O projeto foi construído com foco em práticas comuns no desenvolvimento back-end: autenticação, autorização, persistência relacional, migrations, validação de dados, auditoria, testes automatizados, containerização e integração contínua.

### O que este projeto demonstra

- Construção de uma API REST com FastAPI
- Autenticação baseada em JWT/OAuth2 Password Flow
- Autorização por perfil (**RBAC**)
- Regras de acesso por proprietário do recurso
- Modelagem e persistência com SQLAlchemy e PostgreSQL
- Controle de evolução do banco de dados com Alembic
- Hash de senhas com Argon2
- Validação e serialização com Pydantic
- Histórico de alterações para auditoria
- Testes automatizados com Pytest
- Ambiente reproduzível com Docker Compose
- Integração contínua com GitHub Actions

## Funcionalidades

### Usuários

- Cadastro de usuário
- Login com e-mail e senha
- Consulta do usuário autenticado
- Perfis: `usuario`, `tecnico` e `admin`
- Controle de usuário ativo/inativo
- Área protegida para técnicos
- Área protegida para administradores

### Chamados

- Criar chamado
- Listar chamados
- Consultar chamado por ID
- Atualizar título, descrição e prioridade
- Alterar status (técnico/admin)
- Atribuir técnico (técnico/admin)
- Adicionar e listar comentários
- Consultar histórico de alterações
- Remover chamado respeitando as regras de acesso

### Segurança e autorização

- JWT com expiração
- Senhas armazenadas como hash Argon2
- Endpoints protegidos por autenticação
- Controle de acesso baseado em perfis (RBAC) no servidor
- Usuário comum acessa somente seus próprios chamados
- Técnicos e administradores possuem visão operacional dos chamados
- Segredos configurados por variáveis de ambiente

## Stack tecnológica

| Tecnologia | Utilização |
|---|---|
| Python | Linguagem principal |
| FastAPI | Framework da API REST |
| Pydantic | Validação de dados e schemas |
| SQLAlchemy | ORM e acesso ao banco de dados |
| PostgreSQL | Banco de dados relacional |
| Alembic | Migrations do banco de dados |
| JWT / OAuth2 | Autenticação |
| Argon2 | Hash de senhas |
| Pytest | Testes automatizados |
| Docker Compose | Ambiente de desenvolvimento |
| GitHub Actions | Integração contínua |

## Arquitetura do projeto

```text
DevDesk API
│
├── app/
│   ├── core/
│   │   ├── config.py       # Configurações e ambiente
│   │   ├── database.py     # Sessão e conexão com o banco
│   │   └── security.py     # JWT e hash de senhas
│   │
│   ├── models/             # Modelos SQLAlchemy
│   ├── schemas/            # Schemas Pydantic
│   ├── routers/            # Endpoints e regras HTTP
│   └── main.py             # Inicialização da aplicação
│
├── alembic/                # Migrations do PostgreSQL
├── scripts/                # Scripts auxiliares
├── tests/                  # Testes automatizados
├── docs/                   # Material de portfólio e entrevista
├── Dockerfile
├── compose.yaml
├── requirements.txt
└── .github/workflows/ci.yml
```

## Como executar com Docker

### Pré-requisitos

- Git
- Docker Desktop instalado e em execução

### 1. Clone o repositório

```bash
git clone https://github.com/danielpintorocha10-code/devdesk-api.git
cd devdesk-api
```

### 2. Inicie a aplicação

Na pasta do projeto, execute:

```bash
docker compose up --build
```

O Docker Compose inicia os serviços configurados para a aplicação. A configuração do projeto prevê o PostgreSQL, a aplicação das migrations do Alembic e a inicialização da API.

Na primeira execução, a construção das imagens pode levar alguns minutos.

### 3. Acesse a API

Com os serviços em execução, acesse:

- **API:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health check:** http://localhost:8000/health

### 4. Crie o primeiro administrador

Em outro terminal, na pasta do projeto, execute:

```bash
docker compose exec api python scripts/bootstrap_admin.py
```

Siga as instruções exibidas para informar o nome, o e-mail e a senha do administrador. A senha deve possuir pelo menos 8 caracteres.

### 5. Encerre os serviços

Para parar os serviços, pressione `Ctrl+C` no terminal em que o Docker Compose está executando.

Se quiser encerrar os containers e a rede criada pelo Compose, execute:

```bash
docker compose down
```

> **Segurança:** as credenciais e a chave secreta de demonstração não devem ser utilizadas em produção. Configure segredos fortes e exclusivos antes de qualquer implantação real.

## Executar localmente sem Docker

### 1. Pré-requisitos

Antes de iniciar, instale:

- Python 3.12 ou versão compatível com as dependências do projeto
- PostgreSQL 16
- Git

### 2. Clone o repositório

```bash
git clone https://github.com/danielpintorocha10-code/devdesk-api.git
cd devdesk-api
```

### 3. Crie e ative o ambiente virtual

```bash
python -m venv .venv
```

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

### 4. Instale as dependências

```bash
python -m pip install -r requirements.txt
```

### 5. Configure as variáveis de ambiente

Copie `.env.example` para `.env`.

**Windows (PowerShell):**

```powershell
Copy-Item .env.example .env
```

**Linux/macOS:**

```bash
cp .env.example .env
```

Edite o arquivo `.env` e configure os dados de conexão do PostgreSQL local. Confira se o banco de dados e o usuário existem e se a porta configurada corresponde à sua instalação.

Use uma chave secreta própria para o ambiente de desenvolvimento. Não compartilhe credenciais reais nem publique o arquivo `.env`.

### 6. Execute as migrations e inicie a API

Com o ambiente virtual ativado e o PostgreSQL em execução, execute:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

### 7. Acesse a documentação

Com a API em execução, abra:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc
- **Verificação de saúde:** http://127.0.0.1:8000/health

> **Observação:** a execução local depende de um PostgreSQL acessível e das variáveis definidas no arquivo `.env`. Não utilize credenciais de demonstração em produção.

## Fluxo rápido para demonstrar o projeto

O fluxo abaixo pode ser utilizado como roteiro para uma demonstração em entrevista ou chamada de vídeo:

1. Cadastre um usuário em `POST /usuarios/`.
2. Faça login em `POST /auth/login`.
3. No Swagger, clique em **Authorize** e informe o token.
4. Crie um chamado em `POST /chamados/`.
5. Consulte o chamado em `GET /chamados/{id}`.
6. Adicione um comentário em `POST /chamados/{id}/comentarios`.
7. Use um técnico ou administrador para atribuir o chamado e alterar seu status.
8. Consulte `GET /chamados/{id}/historico` para demonstrar a auditoria.

## Principais endpoints

| Método | Endpoint | Acesso | Finalidade |
|---|---|---|---|
| `POST` | `/usuarios/` | Público | Cadastro |
| `POST` | `/auth/login` | Público | Login e obtenção do token |
| `GET` | `/auth/me` | Autenticado | Consultar perfil atual |
| `POST` | `/chamados/` | Autenticado | Criar chamado |
| `GET` | `/chamados/` | Autenticado | Listar chamados |
| `GET` | `/chamados/{id}` | Autenticado | Consultar chamado |
| `PUT` | `/chamados/{id}` | Dono/técnico/admin | Atualizar chamado |
| `PATCH` | `/chamados/{id}/status` | Técnico/admin | Alterar status |
| `PATCH` | `/chamados/{id}/tecnico` | Técnico/admin | Atribuir técnico |
| `POST` | `/chamados/{id}/comentarios` | Autenticado | Adicionar comentário |
| `GET` | `/chamados/{id}/historico` | Autenticado | Consultar auditoria |
| `DELETE` | `/chamados/{id}` | Dono/admin | Remover chamado |

A documentação interativa da API fica disponível no Swagger em `/docs` quando a aplicação está em execução.

## Testes

Execute a suíte de testes com:

```bash
pytest -q
```

A suíte utiliza um banco SQLite isolado para os testes, permitindo validar as regras principais sem depender de um PostgreSQL externo.

O GitHub Actions está configurado para executar a suíte automaticamente a cada push e pull request.

## Qualidade e segurança

- Segredos não devem ser versionados.
- `.env`, ambientes virtuais, caches e bancos locais devem permanecer no `.gitignore`.
- Senhas não são armazenadas em texto puro.
- Tokens possuem expiração.
- A autorização é validada no back-end, não apenas na interface.
- Regras de propriedade restringem o acesso dos usuários aos chamados de terceiros.
- Alterações importantes geram registros no histórico.

> **Observação:** os valores presentes no `compose.yaml` são destinados ao ambiente local de demonstração. Em produção, credenciais e `SECRET_KEY` devem ser fornecidos por um mecanismo seguro de gerenciamento de segredos.

## Próximas evoluções

Possíveis evoluções para versões futuras:

- Paginação e filtros avançados
- Upload de anexos
- Notificações por e-mail
- Dashboard de indicadores
- Logs estruturados
- Rate limiting
- Deploy em cloud
- Ampliação da cobertura de testes

## Para recrutadores

Este repositório foi desenvolvido para demonstrar fundamentos de **Back-end Júnior**, principalmente API REST, autenticação e autorização, banco de dados relacional, testes automatizados e organização de projeto.

Para conhecer as decisões técnicas e os pontos que podem ser apresentados em uma entrevista, consulte [`docs/ENTREVISTA.md`](docs/ENTREVISTA.md).

## Autor

**Daniel Pinto Rocha**

Projeto desenvolvido para estudo, portfólio e preparação para oportunidades em desenvolvimento Back-end.
