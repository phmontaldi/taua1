import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete

from config import settings
from database import AsyncSessionLocal
from db_models import Turno
from main import app


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def auth_headers():
    return {"X-API-Key": settings.API_KEY}


@pytest_asyncio.fixture(autouse=True)
async def _limpar_turnos():
    yield
    async with AsyncSessionLocal() as db:
        await db.execute(delete(Turno))
        await db.commit()
