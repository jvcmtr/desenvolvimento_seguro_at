

def test_listar_users_positivo(client):
    response = client.get("/users")

    # Assert
    assert response.status_code == 200
    
    dados = response.json()
    assert isinstance(dados, list)
    
    if len(dados) > 0:
        consulta = dados[0]
        assert "id" in consulta
        assert "username" in consulta
        assert "role" in consulta
        assert "password" not in consulta