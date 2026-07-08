from copy import deepcopy

import pytest
from fastapi import status

from conftest import TEST_LIDER_NOME
from models import AuditoriaItem, AuditoriaPayload, ChecklistItem, ChecklistPayload
from services.scoring import compute_auditoria_metrics, compute_checklist_metrics

CHECKLIST_ITEMS = [
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
        "checked": False,
    },
    {
        "id": "eq4",
        "label": "Liquidificador",
        "section_id": "eq",
        "section_title": "1 · Equipamentos",
        "critical": False,
        "checked": True,
    },
]

AUDITORIA_ITEMS = [
    {
        "id": "A1",
        "label": "A1. Qualidade e Consistência do Pré-Batch",
        "section_id": "A",
        "section_title": "A · Organização e Preparo",
        "score": 18,
        "max": 25,
    },
    {
        "id": "A2",
        "label": "A2. Mise en Place de Alto Volume",
        "section_id": "A",
        "section_title": "A · Organização e Preparo",
        "score": 14,
        "max": 20,
    },
    {
        "id": "A3",
        "label": "A3. Organização da Estação para Agilidade",
        "section_id": "A",
        "section_title": "A · Organização e Preparo",
        "score": 10,
        "max": 15,
    },
]


def _montar_payload(date: str = "2025-01-15", bar: str = "piscina") -> dict:
    checklist_items = [ChecklistItem(**item) for item in CHECKLIST_ITEMS]
    auditoria_items = [
        AuditoriaItem(**item, pct=round(item["score"] / item["max"] * 100, 2))
        for item in AUDITORIA_ITEMS
    ]

    checklist_metrics = compute_checklist_metrics(
        ChecklistPayload(
            total=0,
            done=0,
            critical_total=0,
            critical_done=0,
            pct=0,
            critical_pct=0,
            sections=[],
            items=checklist_items,
        )
    )
    auditoria_metrics = compute_auditoria_metrics(
        AuditoriaPayload(total=0, pct=0, classification="", sections=[], items=auditoria_items)
    )

    return {
        "date": date,
        "bar": bar,
        "emocionador": "Equipe Teste",
        "status": "Em Preparação",
        "submitted_at": "2025-01-15T08:45:00Z",
        "checklist": {
            "total": checklist_metrics.total,
            "done": checklist_metrics.done,
            "critical_total": checklist_metrics.critical_total,
            "critical_done": checklist_metrics.critical_done,
            "pct": checklist_metrics.pct,
            "critical_pct": checklist_metrics.critical_pct,
            "sections": [],
            "items": CHECKLIST_ITEMS,
        },
        "auditoria": {
            "total": auditoria_metrics.total,
            "pct": auditoria_metrics.pct,
            "classification": auditoria_metrics.classification,
            "sections": [],
            "items": [item.model_dump() for item in auditoria_items],
        },
    }


async def test_post_turno_feliz(client, auth_headers):
    payload = _montar_payload()

    response = await client.post("/api/v1/turnos", json=payload, headers=auth_headers)

    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body["date"] == payload["date"]
    assert body["bar"] == payload["bar"]
    assert body["checklist_pct"] == payload["checklist"]["pct"]
    assert body["critical_pct"] == payload["checklist"]["critical_pct"]
    assert body["audit_total"] == payload["auditoria"]["total"]
    assert body["audit_pct"] == payload["auditoria"]["pct"]
    assert body["audit_classification"] == payload["auditoria"]["classification"]


async def test_post_turno_ignora_emocionador_do_payload_e_usa_o_do_token(client, auth_headers):
    payload = _montar_payload(date="2025-01-19")
    payload["emocionador"] = "Nome Forjado No Payload"

    response = await client.post("/api/v1/turnos", json=payload, headers=auth_headers)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["emocionador"] == TEST_LIDER_NOME


@pytest.mark.parametrize(
    "campo, novo_valor",
    [
        (("checklist", "pct"), 999.0),
        (("checklist", "critical_pct"), 0.0),
        (("auditoria", "total"), 9999),
        (("auditoria", "pct"), 1.0),
        (("auditoria", "classification"), "Louvor"),
    ],
)
async def test_post_turno_payload_adulterado(client, auth_headers, campo, novo_valor):
    payload = deepcopy(_montar_payload(date="2025-01-16"))
    secao, chave = campo
    payload[secao][chave] = novo_valor

    response = await client.post("/api/v1/turnos", json=payload, headers=auth_headers)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    detail = response.json()["detail"]
    assert "divergencias" in detail
    assert any(d["campo"] == f"{secao}.{chave}" for d in detail["divergencias"])


async def test_post_turno_duplicata_retorna_409_com_turno_existente(client, auth_headers):
    payload = _montar_payload(date="2025-01-17", bar="sport_bar")

    primeira = await client.post("/api/v1/turnos", json=payload, headers=auth_headers)
    assert primeira.status_code == status.HTTP_201_CREATED
    turno_original = primeira.json()

    segunda = await client.post("/api/v1/turnos", json=payload, headers=auth_headers)

    assert segunda.status_code == status.HTTP_409_CONFLICT
    body = segunda.json()
    assert body["turno"]["id"] == turno_original["id"]
    assert body["turno"]["date"] == payload["date"]
    assert body["turno"]["bar"] == payload["bar"]


async def test_get_turnos_sem_token_retorna_401(client):
    response = await client.get("/api/v1/turnos")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_post_turno_sem_token_retorna_401(client):
    payload = _montar_payload(date="2025-01-18")
    response = await client.post("/api/v1/turnos", json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_token_invalido_retorna_401(client):
    response = await client.get(
        "/api/v1/turnos", headers={"Authorization": "Bearer token-invalido"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_health_nao_exige_api_key(client):
    response = await client.get("/api/v1/health")
    assert response.status_code == status.HTTP_200_OK


async def test_get_turnos_filtros_e_paginacao(client, auth_headers):
    for date, bar in [
        ("2025-02-01", "piscina"),
        ("2025-02-02", "piscina"),
        ("2025-02-02", "sport_bar"),
    ]:
        payload = _montar_payload(date=date, bar=bar)
        resposta = await client.post("/api/v1/turnos", json=payload, headers=auth_headers)
        assert resposta.status_code == status.HTTP_201_CREATED

    filtrado_por_bar = await client.get(
        "/api/v1/turnos", params={"bar": "piscina"}, headers=auth_headers
    )
    assert filtrado_por_bar.status_code == status.HTTP_200_OK
    corpo = filtrado_por_bar.json()
    assert corpo["total"] == 2
    assert all(item["bar"] == "piscina" for item in corpo["items"])

    filtrado_por_data = await client.get(
        "/api/v1/turnos", params={"date": "2025-02-02"}, headers=auth_headers
    )
    corpo_data = filtrado_por_data.json()
    assert corpo_data["total"] == 2
    assert all(item["date"] == "2025-02-02" for item in corpo_data["items"])

    paginado = await client.get(
        "/api/v1/turnos", params={"page": 1, "page_size": 2}, headers=auth_headers
    )
    corpo_paginado = paginado.json()
    assert corpo_paginado["total"] == 3
    assert corpo_paginado["page"] == 1
    assert corpo_paginado["page_size"] == 2
    assert corpo_paginado["pages"] == 2
    assert len(corpo_paginado["items"]) == 2
