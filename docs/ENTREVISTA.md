# DevDesk — guia de entrevista técnica

Este documento serve como roteiro de estudo. A ideia é você conseguir explicar o que realmente existe no projeto, sem decorar respostas.

## 1. Pitch de 30 segundos

> O DevDesk é uma API REST de help desk desenvolvida em Python com FastAPI. Usuários abrem chamados, enquanto técnicos e administradores podem atuar no atendimento. Implementei autenticação JWT, autorização por perfis, PostgreSQL com SQLAlchemy e Alembic, comentários, histórico de auditoria, testes com Pytest e ambiente Docker. Também configurei CI com GitHub Actions para automatizar a execução dos testes.

## 2. Por que FastAPI?

Resposta esperada:

> Escolhi FastAPI porque queria praticar construção de APIs REST em Python com tipagem, validação automática e documentação OpenAPI. O framework também facilita a injeção de dependências, que usei para sessão do banco e autenticação.

## 3. Como funciona o login?

Fluxo:

```text
Cliente
  ↓
POST /auth/login
  ↓
Validação do e-mail e senha
  ↓
Verificação do hash Argon2
  ↓
Geração do JWT
  ↓
Cliente envia Bearer Token
  ↓
obter_usuario_atual()
  ↓
Endpoint protegido
```

Ponto importante: a senha não é comparada como texto puro. O projeto armazena um hash e verifica a senha informada contra esse hash.

## 4. O que é RBAC no projeto?

RBAC significa **Role-Based Access Control**.

No DevDesk existem três perfis:

- `usuario`
- `tecnico`
- `admin`

Exemplo:

- usuário comum cria e acompanha seus chamados;
- técnico pode atuar no atendimento;
- administrador possui permissões administrativas.

A regra é aplicada no back-end através das dependências de autenticação/autorização.

## 5. Como você evita que um usuário veja o chamado de outra pessoa?

A API identifica o usuário pelo JWT e compara o `usuario_id` do chamado com o ID do usuário autenticado.

A regra central está em:

```python
def pode_acessar_chamado(chamado, usuario):
    return usuario.perfil in {"tecnico", "admin"} or chamado.usuario_id == usuario.id
```

Isso é uma regra de autorização no servidor. Não depende de uma interface esconder o botão.

## 6. Por que usar Alembic?

> Para controlar a evolução do schema do banco através de migrations versionadas. Assim, as alterações de estrutura podem ser reproduzidas em outros ambientes sem precisar criar as tabelas manualmente.

## 7. Por que usar SQLAlchemy?

> Para trabalhar com o banco através de um ORM, mantendo os modelos Python relacionados às tabelas e permitindo consultas sem escrever SQL para cada operação.

Também é importante saber que ORM não elimina a necessidade de entender SQL e modelagem relacional.

## 8. Por que existe histórico de auditoria?

Quando ações importantes acontecem, como criação de chamado, comentário, alteração de status ou atribuição de técnico, o sistema registra uma entrada no histórico.

Isso ajuda a responder:

- quem fez a alteração;
- qual ação ocorreu;
- qual chamado foi afetado;
- qual descrição foi registrada.

## 9. Por que Docker?

> Para tornar o ambiente reproduzível. O Compose cria a API e o PostgreSQL com configurações consistentes, reduzindo o problema de "na minha máquina funciona".

## 10. Por que testar com SQLite se o projeto usa PostgreSQL?

No projeto, os testes usam um banco SQLite isolado para tornar a suíte rápida e independente de um PostgreSQL externo.

Em uma evolução do projeto, seria interessante adicionar uma suíte de integração com PostgreSQL em container para validar também o comportamento específico do banco utilizado em produção.

## 11. O que você melhoraria em uma próxima versão?

Boas respostas, porque são evoluções coerentes com o projeto:

- paginação;
- filtros por status/prioridade/técnico;
- upload de anexos;
- notificações;
- logs estruturados;
- rate limiting;
- maior cobertura de testes;
- testes de integração com PostgreSQL;
- deploy em cloud.

## 12. Perguntas que você deve saber responder

### JWT

- O que é um JWT?
- Onde o token é enviado?
- O que significa `Bearer`?
- O que acontece quando o token expira?

### API REST

- Diferença entre `POST`, `GET`, `PUT`, `PATCH` e `DELETE`.
- O que representa um status HTTP `200`, `201`, `400`, `401`, `403` e `404`.
- O que é idempotência?

### Banco de dados

- O que é chave primária?
- O que é chave estrangeira?
- O que é relacionamento 1:N?
- Para que serve uma migration?
- Diferença entre ORM e SQL.

### Python/FastAPI

- O que é uma função?
- O que é uma classe?
- O que é uma dependência no FastAPI?
- O que é Pydantic?
- Para que serve `response_model`?

### Git

- O que fazem `git add`, `git commit`, `git push` e `git pull`?
- O que é uma branch?
- O que é um Pull Request?
- Como desfazer uma alteração com segurança?

## 13. O que não falar em entrevista

Evite dizer que uma tecnologia foi usada quando você não sabe explicar minimamente como ela funciona.

Se o entrevistador perguntar algo que você ainda não domina, uma resposta profissional é:

> "Eu implementei essa parte seguindo a documentação e entendo o fluxo principal, mas ainda estou aprofundando esse conceito específico. Posso explicar como ele está sendo usado no projeto."

Isso é melhor do que tentar inventar uma resposta.
