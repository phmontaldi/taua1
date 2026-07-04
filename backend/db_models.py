import uuid
from datetime import date as date_
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    SmallInteger,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Turno(Base):
    __tablename__ = "turno"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    date: Mapped[date_] = mapped_column(Date, nullable=False)
    bar: Mapped[str] = mapped_column(String(15), nullable=False)
    emocionador: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    checklist_total: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    checklist_done: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    checklist_pct: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    critical_total: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    critical_done: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    critical_pct: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    audit_total: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    audit_pct: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    audit_classification: Mapped[str] = mapped_column(String(30), nullable=False)

    items: Mapped[list["TurnoItem"]] = relationship(
        back_populates="turno", cascade="all, delete-orphan"
    )
    auditoria: Mapped[list["TurnoAuditoria"]] = relationship(
        back_populates="turno", cascade="all, delete-orphan"
    )


class TurnoItem(Base):
    __tablename__ = "turno_item"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    turno_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("turno.id", ondelete="CASCADE"), nullable=False
    )
    item_id: Mapped[str] = mapped_column(String(10), nullable=False)
    item_label: Mapped[str] = mapped_column(String(200), nullable=False)
    section_id: Mapped[str] = mapped_column(String(5), nullable=False)
    section_title: Mapped[str] = mapped_column(String(100), nullable=False)
    critical: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    checked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    turno: Mapped["Turno"] = relationship(back_populates="items")


class TurnoAuditoria(Base):
    __tablename__ = "turno_auditoria"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    turno_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("turno.id", ondelete="CASCADE"), nullable=False
    )
    criterio_id: Mapped[str] = mapped_column(String(5), nullable=False)
    criterio_label: Mapped[str] = mapped_column(String(200), nullable=False)
    section_id: Mapped[str] = mapped_column(String(2), nullable=False)
    section_title: Mapped[str] = mapped_column(String(100), nullable=False)
    score: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)
    max_score: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    turno: Mapped["Turno"] = relationship(back_populates="auditoria")
