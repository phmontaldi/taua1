import uuid
from datetime import date as date_
from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, field_validator


class ChecklistSection(BaseModel):
    id: str
    title: str
    total: int
    done: int
    pct: float


class ChecklistItem(BaseModel):
    id: str
    label: str
    section_id: str
    section_title: str
    critical: bool
    checked: bool


class ChecklistPayload(BaseModel):
    total: int
    done: int
    critical_total: int
    critical_done: int
    pct: float
    critical_pct: float
    sections: list[ChecklistSection]
    items: list[ChecklistItem]


class AuditoriaSection(BaseModel):
    id: str
    title: str
    score: int
    max: int
    pct: float


class AuditoriaItem(BaseModel):
    id: str
    label: str
    section_id: str
    section_title: str
    score: int
    max: int
    pct: float


class AuditoriaPayload(BaseModel):
    total: int
    pct: float
    classification: str
    sections: list[AuditoriaSection]
    items: list[AuditoriaItem]


class TurnoCreate(BaseModel):
    date: date_
    bar: Literal["piscina", "sport_bar"]
    emocionador: str
    status: str
    submitted_at: datetime
    checklist: ChecklistPayload
    auditoria: AuditoriaPayload

    @field_validator("emocionador")
    @classmethod
    def emocionador_valido(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("emocionador não pode ser vazio")
        if len(stripped) < 2:
            raise ValueError("emocionador deve ter no mínimo 2 caracteres")
        return stripped

    @field_validator("date")
    @classmethod
    def date_nao_futura(cls, value: date_) -> date_:
        if value > datetime.now(timezone.utc).date():
            raise ValueError("date não pode ser no futuro")
        return value


class TurnoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    date: date_
    bar: str
    emocionador: str
    status: str
    checklist_pct: float
    critical_pct: float
    audit_pct: float
    audit_total: int
    audit_classification: str
    submitted_at: datetime
    created_at: datetime


class TurnoListResponse(BaseModel):
    items: list[TurnoResponse]
    total: int
    page: int
    page_size: int
    pages: int
