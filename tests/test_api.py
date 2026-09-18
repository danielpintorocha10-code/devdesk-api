def cadastrar(client, email="usuario@example.com", senha="Senha1234"):
    response = client.post(
        "/usuarios/",
        json={"nome": "Usuário Teste", "email": email, "senha": senha},
    )
    assert response.status_code == 201
    return response.json()


def login(client, email="usuario@example.com", senha="Senha1234"):
    response = client.post(
        "/auth/login",
        data={"username": email, "password": senha},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_healthcheck(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_cadastro_login_e_perfil(client):
    cadastrar(client)
    token = login(client)

    response = client.get("/auth/me", headers=auth(token))
    assert response.status_code == 200
    assert response.json()["email"] == "usuario@example.com"
    assert response.json()["perfil"] == "usuario"


def test_usuario_cria_e_acessa_apenas_seu_chamado(client):
    cadastrar(client)
    token = login(client)

    criado = client.post(
        "/chamados/",
        json={"titulo": "Notebook não liga", "descricao": "Equipamento sem energia.", "prioridade": "alta"},
        headers=auth(token),
    )
    assert criado.status_code == 201
    chamado = criado.json()
    assert chamado["status"] == "aberto"

    lista = client.get("/chamados/", headers=auth(token))
    assert lista.status_code == 200
    assert len(lista.json()) == 1


def test_usuario_nao_acessa_chamado_de_outro_usuario(client):
    cadastrar(client, "primeiro@example.com")
    token_1 = login(client, "primeiro@example.com")
    chamado = client.post(
        "/chamados/",
        json={"titulo": "Chamado privado", "descricao": "Somente o dono deve acessar.", "prioridade": "media"},
        headers=auth(token_1),
    ).json()

    cadastrar(client, "segundo@example.com")
    token_2 = login(client, "segundo@example.com")

    response = client.get(f"/chamados/{chamado['id']}", headers=auth(token_2))
    assert response.status_code == 403


def test_usuario_pode_comentar_e_consultar_historico(client):
    cadastrar(client)
    token = login(client)
    chamado = client.post(
        "/chamados/",
        json={"titulo": "Teste de comentário", "descricao": "Descrição do teste.", "prioridade": "baixa"},
        headers=auth(token),
    ).json()

    comentario = client.post(
        f"/chamados/{chamado['id']}/comentarios",
        json={"texto": "Estou acompanhando o atendimento."},
        headers=auth(token),
    )
    assert comentario.status_code == 201

    historico = client.get(
        f"/chamados/{chamado['id']}/historico",
        headers=auth(token),
    )
    assert historico.status_code == 200
    assert any(item["acao"] == "criacao" for item in historico.json())
    assert any(item["acao"] == "comentario" for item in historico.json())
