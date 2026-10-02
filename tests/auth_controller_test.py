import pytest
from tests.utils import login_as, logout, login_as_adm, add_user_to_db, remove_user_from_db
from app.models.core.Users import User, UserRole

USERNAME  = "usuario_auth_controller_test"
USER_PASS = "password_auth_controller_test"

@pytest.fixture(scope="module")
def setup_user():
    a = User(
        username=USERNAME, 
        password=USER_PASS, 
        role=UserRole.NENHUM, 
        created_by_user_id=0, 
        created_by="test"
    )
    a = add_user_to_db(a)
    
    yield a
    
    remove_user_from_db(a)


def test_fluxo_login_positivo(client, setup_user):
    user = setup_user
    login_as(client, user.username, USER_PASS)

    response = client.post("/auth/login", json={"username":user.username, "password":USER_PASS})
    assert response.status_code == 200

def test_login_negativo(client, setup_user):
    user = setup_user

    response = client.post("/auth/login", json={"username":user.username, "password":"senha errada"})
    assert response.status_code == 401

    response = client.post("/auth/login", json={"username":"nome errado", "password": USER_PASS})
    assert response.status_code == 401


def test_login_com_mfa_positivo(client, setup_user):
    user = setup_user
    response = client.post("/auth/login", json={"username":user.username, "password":USER_PASS})
    assert response.status_code == 200

    data = response.json()
    assert data["access_token"]
    assert data["mfa_code"]

    response = client.post("/auth/confirm-mfa", json={"username":user.username, "code": data["mfa_code"] })
    assert response.status_code == 200


def test_login_com_mfa_negativo(client, setup_user):
    user = setup_user
    response = client.post("/auth/login", json={"username":user.username, "password":USER_PASS})
    assert response.status_code == 200

    data = response.json()
    assert data["access_token"]
    assert data["mfa_code"]

    response = client.post("/auth/confirm-mfa", json={"username":user.username, "code":"0000" })

    # Se o codigo for invalido o endpoint retorna bad request
    assert response.status_code == 400 