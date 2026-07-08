from sqlalchemy import delete, func, select

from database import AsyncSessionLocal
from db_models import Turno, TurnoAuditoria, TurnoItem
from models import TurnoCreate
from services.turno_service import criar_turno

PAYLOAD = {
    "date": "2025-06-11",
    "bar": "piscina",
    "emocionador": "João Teste",
    "status": "Pronto para Abertura",
    "submitted_at": "2025-06-11T08:45:00Z",
    "checklist": {
        "total": 4,
        "done": 3,
        "pct": 75.0,
        "critical_total": 3,
        "critical_done": 3,
        "critical_pct": 100.0,
        "sections": [
            {"id": "eq", "title": "1 · Equipamentos", "total": 4, "done": 3, "pct": 75.0}
        ],
        "items": [
            {
                "id": "eq1",
                "label": "Máquina de gelo",
                "section_id": "eq",
                "section_title": "1 · Equipamentos",
                "critical": True,
                "checked": True,
            },
            {
                "id": "eq2",
                "label": "Geladeira 1",
                "section_id": "eq",
                "section_title": "1 · Equipamentos",
                "critical": True,
                "checked": True,
            },
            {
                "id": "eq3",
                "label": "Geladeira 2",
                "section_id": "eq",
                "section_title": "1 · Equipamentos",
                "critical": True,
                "checked": True,
            },
            {
                "id": "eq4",
                "label": "Liquidificador",
                "section_id": "eq",
                "section_title": "1 · Equipamentos",
                "critical": False,
                "checked": False,
            },
        ],
    },
    "auditoria": {
        "total": 42,
        "pct": 70.0,
        "classification": "Regular",
        "sections": [
            {
                "id": "A",
                "title": "A · Organização e Preparo",
                "score": 42,
                "max": 60,
                "pct": 70.0,
            }
        ],
        "items": [
            {
                "id": "A1",
                "label": "A1. Qualidade e Consistência do Pré-Batch",
                "section_id": "A",
                "section_title": "A · Organização e Preparo",
                "score": 18,
                "max": 25,
                "pct": 72.0,
            },
            {
                "id": "A2",
                "label": "A2. Mise en Place de Alto Volume",
                "section_id": "A",
                "section_title": "A · Organização e Preparo",
                "score": 14,
                "max": 20,
                "pct": 70.0,
            },
            {
                "id": "A3",
                "label": "A3. Organização da Estação para Agilidade",
                "section_id": "A",
                "section_title": "A · Organização e Preparo",
                "score": 10,
                "max": 15,
                "pct": 66.7,
            },
        ],
    },
}


async def test_criar_turno_insere_turno_itens_e_auditoria_em_transacao_unica():
    payload = TurnoCreate(**PAYLOAD)

    async with AsyncSessionLocal() as db:
        turno = await criar_turno(db, payload)

        try:
            assert turno.id is not None

            itens_count = await db.scalar(
                select(func.count())
                .select_from(TurnoItem)
                .where(TurnoItem.turno_id == turno.id)
            )
            assert itens_count == 4

            auditoria_count = await db.scalar(
                select(func.count())
                .select_from(TurnoAuditoria)
                .where(TurnoAuditoria.turno_id == turno.id)
            )
            assert auditoria_count == 3

            eq4 = await db.scalar(
                select(TurnoItem).where(
                    TurnoItem.turno_id == turno.id, TurnoItem.item_id == "eq4"
                )
            )
            assert eq4.checked is False
        finally:
            await db.execute(delete(Turno).where(Turno.id == turno.id))
            await db.commit()
