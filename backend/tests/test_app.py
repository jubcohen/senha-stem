import pytest
from backend.app import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_login_sucesso(client):
    resposta = client.post("/login", json={"usuario": "admin", "senha": "senha123"})
    assert resposta.status_code == 200
    assert resposta.json["mensagem"] == "Login bem-sucedido"

def test_login_falha(client):
    resposta = client.post("/login", json={"usuario": "admin", "senha": "errada"})
    assert resposta.status_code == 401
    assert "erro" in resposta.json
