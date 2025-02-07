import pytest
import json
from app import app  # Importa o Flask app

@pytest.fixture
def client():
    return app.test_client()

@pytest.mark.parametrize("cpf, data_nasc, senha, esperado", [
    ("123.456.789-09", "2000-05-15", "Senha@12", 200),  # Teste de Senha Válida
    ("123.456.789-09", "2000-05-15", "Sen@1", 400),  # Menos de 8 caracteres
    ("123.456.789-09", "2000-05-15", "senha@12", 400),  # Falta Letra Maiúscula
    ("123.456.789-09", "2000-05-15", "SENHA@12", 400),  # Falta Letra Minúscula
    ("123.456.789-09", "2000-05-15", "Senha@ab", 400),  # Falta Número
    ("123.456.789-09", "2000-05-15", "Senha1267", 400),  # Falta Caractere Especial
    ("123.456.789-09", "2000-05-15", "Senha@1732684292737438284293", 400),  # Mais de 20 Caracteres
    ("123.456.789-09", "2000-05-15", "Senha @12", 400),  # Contém Espaços
    ("123.456.789-09", "2000-05-15", "Senha@1111", 400),  # Repetição Excessiva de Caracteres
    ("123.456.789-09", "2000-05-15", "Senha@abcd", 400),  # Sequência Numérica ou Alfabética
    ("123.456.789-09", "2000-05-15", "123.456.789-09Senha@12", 400),  # Contém CPF
    ("123.456.789-09", "2000-05-15", "2000-05-15Senha@", 400),  # Contém Data de Nascimento
])
def test_validar_senha(client, cpf, data_nasc, senha, esperado):
    response = client.post("/validar-senha", json={
        "cpf": cpf,
        "data_nasc": data_nasc,
        "senha": senha
    })
    print(response.json)  # Para debug
    assert response.status_code == esperado
