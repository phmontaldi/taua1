from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from db_models import Turno, TurnoAuditoria, TurnoItem
from models import TurnoCreate


async def criar_turno(db: AsyncSession, payload: TurnoCreate) -> Turno:
    turno = Turno(
        date=payload.date,
        bar=payload.bar,
        emocionador=payload.emocionador,
        status=payload.status,
        submitted_at=payload.submitted_at,
        checklist_total=payload.checklist.total,
        checklist_done=payload.checklist.done,
        checklist_pct=payload.checklist.pct,
        critical_total=payload.checklist.critical_total,
        critical_done=payload.checklist.critical_done,
        critical_pct=payload.checklist.critical_pct,
        audit_total=payload.auditoria.total,
        audit_pct=payload.auditoria.pct,
        audit_classification=payload.auditoria.classification,
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
    except Exception:
        await db.rollback()
        raise

    return turno
