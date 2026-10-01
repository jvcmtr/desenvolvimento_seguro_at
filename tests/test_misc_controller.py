from tests.utils import login_as, logout, login_as_adm, add_user_to_db, remove_user_from_db
from app.models.core.Users import User, UserRole


def test_adm_ping_negativo(client):
    # Rota protegida
    response = client.get("/adm-ping")
    assert response.status_code == 401

    USERNAME = "test_adm_ping_negativo"
    PASSWORD = "123" # ao criar o usuario no banco a senha é hasheada, alterando a instancia original

    user = User(
        username=USERNAME, 
        password=PASSWORD, 
        role=UserRole.NENHUM,
        created_by_user_id = 0, 
        created_by="test_misc_controller.py"
    ) 
    add_user_to_db(user)

    login_as(client, USERNAME, PASSWORD)

    # Usuario com role NENHUM não autorizado
    response = client.get("/adm-ping")
    assert response.status_code == 403

    remove_user_from_db(user)
    logout(client)

def test_adm_ping_positivo(client):
    login_as_adm(client)
    response = client.get("/adm-ping")
    assert response.status_code == 200