import pytest
from fastapi.testclient import TestClient
from tests.utils import login_as, login_as_adm, add_user_to_db, remove_user_from_db
from app.models.core.Users import User, UserRole

# -----------------
#  Para poder ver a descrições detalhadas das 
#  test_vulnerabilidades testadas acesse /docs/threat_model.md
# -----------------

USER_A_USERNAME = "username_A"
USER_B_USERNAME = "username_B"
USER_PASS = "senha123"

@pytest.fixture(scope="module")
def setup_users():
    user_a = User(username=USER_A_USERNAME, password=USER_PASS, role=UserRole.NENHUM, created_by_user_id=0, created_by="test")
    user_b = User(username=USER_B_USERNAME, password=USER_PASS, role=UserRole.NENHUM, created_by_user_id=0, created_by="test")
    
    user_a = add_user_to_db(user_a)
    user_b = add_user_to_db(user_b)
    
    yield user_a, user_b
    
    remove_user_from_db(user_a)
    remove_user_from_db(user_b)


def test_vuln06_criacao_admin_bloqueada(client):
    payload = {
        "username": "hacker_admin",
        "password": "hackersPassword123",
        "role": UserRole.ADMIN.value
    }
    
    response = client.post("/users/", json=payload)
    assert response.status_code == 403


def test_vuln06_atualizacao_admin_bloqueada(client, setup_users):
    user_a, _ = setup_users
    login_as(client, USER_A_USERNAME, USER_PASS)
    
    payload = {
        "id": 0,
        "username": USER_A_USERNAME,
        "password": "newpassword123",
        "role": UserRole.ADMIN.value
    }
    
    response = client.put(f"/users/{user_a.id}", json=payload)
    assert response.status_code == 403



def test_vuln04_leitura_terceiros(client, setup_users):
    user_a, user_b = setup_users
    
    # faz login com usuario A
    login_as(client, USER_A_USERNAME, USER_PASS)

    # Tenta acessar o usuario B
    response = client.get(f"/users/{user_b.id}")
    assert response.status_code == 403


def test_vuln02_modificacao_terceiros(client, setup_users):
    user_a, user_b = setup_users
    
    # faz login com usuario A
    login_as(client, USER_A_USERNAME, USER_PASS)
    
    # tenta deletar usuario B
    response = client.delete(f"/users/{user_b.id}")
    assert response.status_code == 403


def test_acesso_admin_permitido_para_qualquer_registro(client, setup_users):
    _, user_b = setup_users
    
    # faz login como admin
    login_as_adm(client)

    # Tenta acessar o usuario B
    response = client.get(f"/users/{user_b.id}")
    
    # Admin lendo Usuário B
    response = client.get(f"/users/{user_b.id}")
    assert response.status_code == 200
    assert response.json()["username"] == USER_B_USERNAME