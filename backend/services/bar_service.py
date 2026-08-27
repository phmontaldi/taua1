from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db_models import Bar


async def listar_bares_ativos(db: AsyncSession) -> list[Bar]:
    resultado = await db.scalars(select(Bar).where(Bar.ativo.is_(True)).order_by(Bar.id))
    return list(resultado.all())


async def validar_bar(db: AsyncSession, slug: str, *, exigir_ativo: bool = True) -> Bar:
    """Valida o slug contra a tabela `bar`, levantando 422 com mensagem clara.

    Com exigir_ativo=False aceita bares inativos (útil para consultar histórico).
    """
    bar = await db.scalar(select(Bar).where(Bar.slug == slug))
    if bar is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail={"message": f"Bar '{slug}' não existe."},
        )
    if exigir_ativo and not bar.ativo:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail={"message": f"Bar '{slug}' está inativo e não aceita novos envios."},
        )
    return bar
