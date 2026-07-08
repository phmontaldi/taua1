from datetime import timedelta

from fastapi import status

from conftest import TEST_LIDER_NOME, TEST_LIDER_PIN, gerar_token
from database import AsyncSessionLocal
from db_models import Lider


async def test_login_feliz(client, lider_teste):
    response = await client.post(
        "/api/v1/auth/login", json={"nome": TEST_LIDER_NOME, "pin": TEST_LIDER_PIN}
    )

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["nome"] == TEST_LIDER_NOME
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert body["expires_at"]


async def test_login_pin_errado_retorna_401(client, lider_teste):
    response = await client.post(
        "/api/v1/auth/login", json={"nome": TEST_LIDER_NOME, "pin": "0000"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_login_lider_inativo_retorna_401(client, lider_teste):
    async with AsyncSessionLocal() as db:
        lider = await db.get(Lider, lider_teste.id)
        lider.ativo = False
        await db.commit()

    response = await client.post(
        "/api/v1/auth/login", json={"nome": TEST_LIDER_NOME, "pin": TEST_LIDER_PIN}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_login_nome_inexistente_retorna_401(client):
    response = await client.post(
        "/api/v1/auth/login", json={"nome": "Ninguem Cadastrado", "pin": "1234"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_token_expirado_retorna_401(client, lider_teste):
    token = gerar_token(lider_teste, expira_em=timedelta(seconds=-1))

    response = await client.get(
        "/api/v1/turnos", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Token expirado"


async def test_rota_protegida_sem_token_retorna_401(client):
    response = await client.get("/api/v1/turnos")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Token ausente ou inválido"
