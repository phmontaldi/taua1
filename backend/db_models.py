import datetime
import uuid

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Computed,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    SmallInteger,
    String,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Turno(Base):
    __tablename__ = "turno"
    __table_args__ = (
        CheckConstraint("bar IN ('piscina', 'sport_bar')", name="turno_bar_check"),
        Index("idx_turno_date", "date"),
        Index("idx_turno_bar", "bar"),
        Index("idx_turno_date_bar", "date", "bar"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    bar: Mapped[str] = mapped_column(String(15), nullable=False)
    emocionador: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    submitted_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("NOW()")
    )
    checklist_total: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    checklist_done: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    checklist_pct: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    critical_total: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    critical_done: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    critical_pct: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    audit_total: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    audit_pct: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    audit_classification: Mapped[str] = mapped_column(String(30), nullable=False)

    itens: Mapped[list["TurnoItem"]] = relationship(
        back_populates="turno", cascade="all, delete-orphan", passive_deletes=True
    )
    auditorias: Mapped[list["TurnoAuditoria"]] = relationship(
        back_populates="turno", cascade="all, delete-orphan", passive_deletes=True
    )


class TurnoItem(Base):
    __tablename__ = "turno_item"
    __table_args__ = (
        Index("idx_item_turno_id", "turno_id"),
        Index("idx_item_section", "section_id"),
        Index("idx_item_checked", "checked", postgresql_where=text("checked = FALSE")),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    turno_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("turno.id", ondelete="CASCADE"), nullable=False
    )
    item_id: Mapped[str] = mapped_column(String(10), nullable=False)
    item_label: Mapped[str] = mapped_column(String(200), nullable=False)
    section_id: Mapped[str] = mapped_column(String(5), nullable=False)
    section_title: Mapped[str] = mapped_column(String(100), nullable=False)
    critical: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text("FALSE"))
    checked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text("FALSE"))

    turno: Mapped["Turno"] = relationship(back_populates="itens")


class TurnoAuditoria(Base):
    __tablename__ = "turno_auditoria"
    __table_args__ = (
        Index("idx_audit_turno_id", "turno_id"),
        Index("idx_audit_criterio", "criterio_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    turno_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("turno.id", ondelete="CASCADE"), nullable=False
    )
    criterio_id: Mapped[str] = mapped_column(String(5), nullable=False)
    criterio_label: Mapped[str] = mapped_column(String(200), nullable=False)
    section_id: Mapped[str] = mapped_column(String(2), nullable=False)
    section_title: Mapped[str] = mapped_column(String(100), nullable=False)
    score: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0, server_default=text("0"))
    max_score: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    pct: Mapped[float] = mapped_column(
        Numeric(5, 2),
        Computed("ROUND(score::NUMERIC / NULLIF(max_score, 0) * 100, 2)", persisted=True),
    )

    turno: Mapped["Turno"] = relationship(back_populates="auditorias")
