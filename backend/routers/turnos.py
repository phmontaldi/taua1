import math
from datetime import date as date_
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from auth import LiderAtual, get_current_lider
from database import get_db
from models import TurnoCreate, TurnoListResponse, TurnoResponse
from services.scoring import (
    comparar_auditoria,
    comparar_checklist,
    compute_auditoria_metrics,
    compute_checklist_metrics,
)
from services.turno_service import TurnoDuplicadoError, criar_turno, listar_turnos

router = APIRouter(prefix="/api/v1/turnos", tags=["turnos"])


@router.post("", response_model=TurnoResponse, status_code=status.HTTP_201_CREATED)
async def criar_turno_endpoint(
    payload: TurnoCreate,
    db: AsyncSession = Depends(get_db),
    lider: LiderAtual = Depends(get_current_lider),
):
    payload = payload.model_copy(update={"emocionador": lider.nome})

    checklist_metrics = compute_checklist_metrics(payload.checklist)
    auditoria_metrics = compute_auditoria_metrics(payload.auditoria)

    divergencias = comparar_checklist(checklist_metrics, payload.checklist) + comparar_auditoria(
        auditoria_metrics, payload.auditoria
    )
    if divergencias:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail={
                "message": "Os agregados enviados divergem dos itens de checklist/auditoria.",
                "divergencias": divergencias,
            },
        )

    try:
        turno = await criar_turno(db, payload)
    except TurnoDuplicadoError as exc:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "message": (
                    f"Já existe um turno para bar={payload.bar} date={payload.date.isoformat()}."
                ),
                "turno": TurnoResponse.model_validate(exc.turno).model_dump(mode="json"),
            },
        )

    return turno


@router.get("", response_model=TurnoListResponse)
async def listar_turnos_endpoint(
    date: date_ | None = None,
    bar: Literal["piscina", "sport_bar"] | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    turnos, total = await listar_turnos(db, date=date, bar=bar, page=page, page_size=page_size)
    pages = math.ceil(total / page_size) if total else 0

    return TurnoListResponse(
        items=[TurnoResponse.model_validate(t) for t in turnos],
        total=total,
        page=page,
        page_size=page_size,
        pages=pages,
    )
