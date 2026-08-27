from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import BarResponse
from services.bar_service import listar_bares_ativos

router = APIRouter(prefix="/api/v1/bares", tags=["bares"])


@router.get("", response_model=list[BarResponse])
async def listar_bares_endpoint(db: AsyncSession = Depends(get_db)):
    """Lista os bares ativos (autenticação exigida pelo JWTAuthMiddleware)."""
    return await listar_bares_ativos(db)
