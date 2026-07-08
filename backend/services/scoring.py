"""Recomputo server-side dos agregados de checklist e auditoria.

Os totais/percentuais enviados pelo cliente em TurnoCreate nunca são
persistidos diretamente: são sempre recalculados a partir dos itens de
checklist e dos critérios de auditoria, que são a fonte de verdade.
"""

from dataclasses import dataclass

from models import AuditoriaPayload, ChecklistPayload

TOLERANCIA_PCT = 0.01

_ESCALA_CLASSIFICACAO = (
    (190, "Louvor"),
    (170, "Muito Bom"),
    (150, "Bom"),
    (120, "Regular"),
    (80, "Insuficiente"),
    (0, "Deficiente"),
)


@dataclass(frozen=True)
class ChecklistMetrics:
    total: int
    done: int
    pct: float
    critical_total: int
    critical_done: int
    critical_pct: float


@dataclass(frozen=True)
class AuditoriaMetrics:
    total: int
    max: int
    pct: float
    classification: str


def _pct(numerador: int, denominador: int) -> float:
    if denominador == 0:
        return 0.0
    return round(numerador / denominador * 100, 2)


def classificar(total_pontos: int) -> str:
    for minimo, label in _ESCALA_CLASSIFICACAO:
        if total_pontos >= minimo:
            return label
    return _ESCALA_CLASSIFICACAO[-1][1]


def compute_checklist_metrics(checklist: ChecklistPayload) -> ChecklistMetrics:
    total = len(checklist.items)
    done = sum(1 for item in checklist.items if item.checked)
    criticos = [item for item in checklist.items if item.critical]
    critical_total = len(criticos)
    critical_done = sum(1 for item in criticos if item.checked)
    return ChecklistMetrics(
        total=total,
        done=done,
        pct=_pct(done, total),
        critical_total=critical_total,
        critical_done=critical_done,
        critical_pct=_pct(critical_done, critical_total),
    )


def compute_auditoria_metrics(auditoria: AuditoriaPayload) -> AuditoriaMetrics:
    total = sum(item.score for item in auditoria.items)
    maximo = sum(item.max for item in auditoria.items)
    return AuditoriaMetrics(
        total=total,
        max=maximo,
        pct=_pct(total, maximo),
        classification=classificar(total),
    )


def comparar_checklist(metrics: ChecklistMetrics, checklist: ChecklistPayload) -> list[dict]:
    divergencias = []
    if abs(checklist.pct - metrics.pct) > TOLERANCIA_PCT:
        divergencias.append(
            {"campo": "checklist.pct", "enviado": checklist.pct, "calculado": metrics.pct}
        )
    if abs(checklist.critical_pct - metrics.critical_pct) > TOLERANCIA_PCT:
        divergencias.append(
            {
                "campo": "checklist.critical_pct",
                "enviado": checklist.critical_pct,
                "calculado": metrics.critical_pct,
            }
        )
    return divergencias


def comparar_auditoria(metrics: AuditoriaMetrics, auditoria: AuditoriaPayload) -> list[dict]:
    divergencias = []
    if auditoria.total != metrics.total:
        divergencias.append(
            {"campo": "auditoria.total", "enviado": auditoria.total, "calculado": metrics.total}
        )
    if abs(auditoria.pct - metrics.pct) > TOLERANCIA_PCT:
        divergencias.append(
            {"campo": "auditoria.pct", "enviado": auditoria.pct, "calculado": metrics.pct}
        )
    if auditoria.classification != metrics.classification:
        divergencias.append(
            {
                "campo": "auditoria.classification",
                "enviado": auditoria.classification,
                "calculado": metrics.classification,
            }
        )
    return divergencias
