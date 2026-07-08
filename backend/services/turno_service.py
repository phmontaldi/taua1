from datetime import date as date_

from sqlalchemy import func, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db_models import Turno, TurnoAuditoria, TurnoItem
from models import TurnoCreate
from services.scoring import compute_auditoria_metrics, compute_checklist_metrics


class TurnoDuplicadoError(Exception):
    """Levantada quando já existe um turno para a mesma (date, bar)."""

    def __init__(self, turno: Turno):
        self.turno = turno
        super().__init__(f"Turno duplicado para date={turno.date} bar={turno.bar}")


async def criar_turno(db: AsyncSession, payload: TurnoCreate) -> Turno:
    checklist_metrics = compute_checklist_metrics(payload.checklist)
    auditoria_metrics = compute_auditoria_metrics(payload.auditoria)

    turno = Turno(
        date=payload.date,
        bar=payload.bar,
        emocionador=payload.emocionador,
        status=payload.status,
        submitted_at=payload.submitted_at,
        checklist_total=checklist_metrics.total,
        checklist_done=checklist_metrics.done,
        checklist_pct=checklist_metrics.pct,
        critical_total=checklist_metrics.critical_total,
        critical_done=checklist_metrics.critical_done,
        critical_pct=checklist_metrics.critical_pct,
        audit_total=auditoria_metrics.total,
        audit_pct=auditoria_metrics.pct,
        audit_classification=auditoria_metrics.classification,
    )

    try:
        db.add(turno)
        await db.flush()

        if payload.checklist.items:
            await db.execute(
                insert(TurnoItem),
                [
                    {
                        "turno_id": turno.id,
                        "item_id": item.id,
                        "item_label": item.label,
                        "section_id": item.section_id,
                        "section_title": item.section_title,
                        "critical": item.critical,
                        "checked": item.checked,
                    }
                    for item in payload.checklist.items
                ],
            )

        if payload.auditoria.items:
            await db.execute(
                insert(TurnoAuditoria),
                [
                    {
                        "turno_id": turno.id,
                        "criterio_id": item.id,
                        "criterio_label": item.label,
                        "section_id": item.section_id,
                        "section_title": item.section_title,
                        "score": item.score,
                        "max_score": item.max,
                    }
                    for item in payload.auditoria.items
                ],
            )

        await db.commit()
    except IntegrityError:
        await db.rollback()
        existente = await db.scalar(
            select(Turno).where(Turno.date == payload.date, Turno.bar == payload.bar)
        )
        if existente is not None:
            raise TurnoDuplicadoError(existente) from None
        raise
    except Exception:
        await db.rollback()
        raise

    return turno


async def listar_turnos(
    db: AsyncSession,
    *,
    date: date_ | None = None,
    bar: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[Turno], int]:
    filtros = []
    if date is not None:
        filtros.append(Turno.date == date)
    if bar is not None:
        filtros.append(Turno.bar == bar)

    total = await db.scalar(select(func.count()).select_from(Turno).where(*filtros)) or 0

    resultado = await db.scalars(
        select(Turno)
        .where(*filtros)
        .order_by(Turno.date.desc(), Turno.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    return list(resultado.all()), total
