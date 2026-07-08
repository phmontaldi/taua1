import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import jwt
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from passlib.context import CryptContext
from sqlalchemy import delete

from auth import JWT_ALGORITHM
from config import settings
from database import AsyncSessionLocal
from db_models import Lider, Turno
from main import app
from rate_limit import limiter

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

TEST_LIDER_NOME = "Emocionador Teste"
TEST_LIDER_PIN = "1234"


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def lider_teste():
    async with AsyncSessionLocal() as db:
        lider = Lider(
            nome=TEST_LIDER_NOME, pin_hash=pwd_context.hash(TEST_LIDER_PIN), ativo=True
        )
        db.add(lider)
        await db.commit()
        await db.refresh(lider)

    yield lider

    async with AsyncSessionLocal() as db:
        await db.execute(delete(Lider).where(Lider.id == lider.id))
        await db.commit()


@pytest.fixture
def auth_headers(lider_teste):
    return {"Authorization": f"Bearer {gerar_token(lider_teste)}"}


def gerar_token(lider, *, expira_em: timedelta = timedelta(days=1)) -> str:
    return jwt.encode(
        {
            "sub": str(lider.id),
            "nome": lider.nome,
            "exp": datetime.now(timezone.utc) + expira_em,
        },
        settings.JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )


@pytest_asyncio.fixture(autouse=True)
async def _limpar_turnos():
    limiter.reset()
    yield
    async with AsyncSessionLocal() as db:
        await db.execute(delete(Turno))
        await db.commit()
