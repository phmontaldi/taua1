from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, Depends, HTTPException, Request, status
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth import JWT_ALGORITHM
from config import settings
from database import get_db
from db_models import Lider
from models import LoginRequest, LoginResponse
from rate_limit import limiter

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_EXPIRATION = timedelta(days=30)


@router.post("/login", response_model=LoginResponse)
@limiter.limit("5/minute")
async def login(
    request: Request, payload: LoginRequest, db: AsyncSession = Depends(get_db)
):
    lider = await db.scalar(select(Lider).where(Lider.nome == payload.nome))

    if lider is None:
        pwd_context.dummy_verify()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Nome ou PIN inválidos"
        )

    if not lider.ativo or not pwd_context.verify(payload.pin, lider.pin_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Nome ou PIN inválidos"
        )

    expira_em = datetime.now(timezone.utc) + JWT_EXPIRATION
    token = jwt.encode(
        {"sub": str(lider.id), "nome": lider.nome, "exp": expira_em},
        settings.JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )

    return LoginResponse(
        access_token=token, token_type="bearer", nome=lider.nome, expires_at=expira_em
    )
