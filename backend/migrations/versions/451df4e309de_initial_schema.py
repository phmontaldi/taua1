"""initial schema

Revision ID: 451df4e309de
Revises:
Create Date: 2026-07-04 17:11:05.352866

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '451df4e309de'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto"')

    op.create_table(
        'turno',
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('bar', sa.String(length=15), nullable=False),
        sa.Column('emocionador', sa.String(length=100), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('checklist_total', sa.SmallInteger(), nullable=False),
        sa.Column('checklist_done', sa.SmallInteger(), nullable=False),
        sa.Column('checklist_pct', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('critical_total', sa.SmallInteger(), nullable=False),
        sa.Column('critical_done', sa.SmallInteger(), nullable=False),
        sa.Column('critical_pct', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('audit_total', sa.SmallInteger(), nullable=False),
        sa.Column('audit_pct', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('audit_classification', sa.String(length=30), nullable=False),
        sa.CheckConstraint("bar IN ('piscina', 'sport_bar')", name='turno_bar_check'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_turno_date', 'turno', ['date'], unique=False)
    op.create_index('idx_turno_bar', 'turno', ['bar'], unique=False)
    op.create_index('idx_turno_date_bar', 'turno', ['date', 'bar'], unique=False)

    op.create_table(
        'turno_item',
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('turno_id', sa.UUID(), nullable=False),
        sa.Column('item_id', sa.String(length=10), nullable=False),
        sa.Column('item_label', sa.String(length=200), nullable=False),
        sa.Column('section_id', sa.String(length=5), nullable=False),
        sa.Column('section_title', sa.String(length=100), nullable=False),
        sa.Column('critical', sa.Boolean(), server_default=sa.text('FALSE'), nullable=False),
        sa.Column('checked', sa.Boolean(), server_default=sa.text('FALSE'), nullable=False),
        sa.ForeignKeyConstraint(['turno_id'], ['turno.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_item_turno_id', 'turno_item', ['turno_id'], unique=False)
    op.create_index('idx_item_section', 'turno_item', ['section_id'], unique=False)
    op.create_index(
        'idx_item_checked', 'turno_item', ['checked'], unique=False,
        postgresql_where=sa.text('checked = FALSE'),
    )

    op.create_table(
        'turno_auditoria',
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('turno_id', sa.UUID(), nullable=False),
        sa.Column('criterio_id', sa.String(length=5), nullable=False),
        sa.Column('criterio_label', sa.String(length=200), nullable=False),
        sa.Column('section_id', sa.String(length=2), nullable=False),
        sa.Column('section_title', sa.String(length=100), nullable=False),
        sa.Column('score', sa.SmallInteger(), server_default=sa.text('0'), nullable=False),
        sa.Column('max_score', sa.SmallInteger(), nullable=False),
        sa.Column(
            'pct', sa.Numeric(precision=5, scale=2),
            sa.Computed('ROUND(score::NUMERIC / NULLIF(max_score, 0) * 100, 2)', persisted=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(['turno_id'], ['turno.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_audit_turno_id', 'turno_auditoria', ['turno_id'], unique=False)
    op.create_index('idx_audit_criterio', 'turno_auditoria', ['criterio_id'], unique=False)

    op.execute("""
        CREATE OR REPLACE VIEW v_resumo_turno AS
        SELECT
          t.id,
          t.date,
          EXTRACT(YEAR  FROM t.date)::INT  AS ano,
          EXTRACT(MONTH FROM t.date)::INT  AS mes,
          EXTRACT(WEEK  FROM t.date)::INT  AS semana_ano,
          TO_CHAR(t.date, 'YYYY-MM')      AS ano_mes,
          TRIM(TO_CHAR(t.date, 'Day'))    AS dia_semana,
          t.bar,
          t.emocionador,
          t.status,
          t.submitted_at,
          t.checklist_total,
          t.checklist_done,
          t.checklist_pct,
          t.critical_total,
          t.critical_done,
          t.critical_pct,
          (t.critical_total - t.critical_done) AS critical_faltantes,
          t.audit_total,
          t.audit_pct,
          t.audit_classification
        FROM turno t
    """)

    op.execute("""
        CREATE OR REPLACE VIEW v_itens_faltantes AS
        SELECT
          t.date,
          t.bar,
          t.emocionador,
          t.status,
          ti.section_id,
          ti.section_title,
          ti.item_id,
          ti.item_label,
          ti.critical
        FROM turno t
        JOIN turno_item ti ON t.id = ti.turno_id
        WHERE ti.checked = FALSE
        ORDER BY t.date DESC, ti.critical DESC, ti.section_id
    """)

    op.execute("""
        CREATE OR REPLACE VIEW v_auditoria_detalhada AS
        SELECT
          t.id AS turno_id,
          t.date,
          t.bar,
          t.emocionador,
          ta.section_id,
          ta.section_title,
          ta.criterio_id,
          ta.criterio_label,
          ta.score,
          ta.max_score,
          ta.pct
        FROM turno t
        JOIN turno_auditoria ta ON t.id = ta.turno_id
        ORDER BY t.date DESC, ta.criterio_id
    """)

    op.execute("""
        CREATE OR REPLACE VIEW v_frequencia_falta_item AS
        SELECT
          ti.item_id,
          ti.item_label,
          ti.section_id,
          ti.section_title,
          ti.critical,
          COUNT(*) AS total_turnos,
          SUM(CASE WHEN ti.checked = FALSE THEN 1 ELSE 0 END) AS vezes_faltou,
          ROUND(
            SUM(CASE WHEN ti.checked = FALSE THEN 1 ELSE 0 END)::NUMERIC
            / COUNT(*) * 100, 1
          ) AS pct_falta
        FROM turno_item ti
        JOIN turno t ON t.id = ti.turno_id
        WHERE t.date >= CURRENT_DATE - INTERVAL '30 days'
        GROUP BY ti.item_id, ti.item_label, ti.section_id, ti.section_title, ti.critical
        ORDER BY pct_falta DESC
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('DROP VIEW IF EXISTS v_frequencia_falta_item')
    op.execute('DROP VIEW IF EXISTS v_auditoria_detalhada')
    op.execute('DROP VIEW IF EXISTS v_itens_faltantes')
    op.execute('DROP VIEW IF EXISTS v_resumo_turno')

    op.drop_index('idx_audit_criterio', table_name='turno_auditoria')
    op.drop_index('idx_audit_turno_id', table_name='turno_auditoria')
    op.drop_table('turno_auditoria')

    op.drop_index('idx_item_checked', table_name='turno_item', postgresql_where=sa.text('checked = FALSE'))
    op.drop_index('idx_item_section', table_name='turno_item')
    op.drop_index('idx_item_turno_id', table_name='turno_item')
    op.drop_table('turno_item')

    op.drop_index('idx_turno_date_bar', table_name='turno')
    op.drop_index('idx_turno_bar', table_name='turno')
    op.drop_index('idx_turno_date', table_name='turno')
    op.drop_table('turno')
