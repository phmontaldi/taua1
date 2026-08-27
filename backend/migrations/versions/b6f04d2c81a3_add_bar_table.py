"""add bar table, seed bares e troca CHECK por FK em turno.bar

Cria a tabela `bar` como cadastro dos bares (antes valores fixos no código),
popula com os bares existentes e os novos, remove o CHECK `turno_bar_check`
e o substitui por FK `turno.bar -> bar.slug`, preservando os registros
existentes de `turno`. Também expõe o rótulo do bar nas views do Power BI
(coluna `bar_rotulo` adicionada ao final, mantendo as colunas existentes).

Obs.: o downgrade recria o CHECK original e portanto falha se existirem
turnos de bares fora de ('piscina', 'sport_bar').

Revision ID: b6f04d2c81a3
Revises: 1d25e89ab441
Create Date: 2026-08-27 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b6f04d2c81a3'
down_revision: Union[str, Sequence[str], None] = '1d25e89ab441'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
    CREATE TABLE bar (
      id         SERIAL       PRIMARY KEY,
      slug       VARCHAR(15)  NOT NULL UNIQUE,
      rotulo     VARCHAR(60)  NOT NULL,
      ativo      BOOLEAN      NOT NULL DEFAULT TRUE,
      created_at TIMESTAMPTZ  NOT NULL DEFAULT NOW()
    );
    """)

    op.execute("""
    INSERT INTO bar (slug, rotulo) VALUES
      ('piscina',    'Bar da Piscina'),
      ('sport_bar',  'Sport Bar'),
      ('ondas_1',    'Bar Ondas 1'),
      ('rooftop',    'Rooftop'),
      ('nigori',     'Nigori'),
      ('coppolla',   'Coppolla'),
      ('beach_club', 'Beach Club');
    """)

    op.execute("ALTER TABLE turno DROP CONSTRAINT turno_bar_check;")
    op.execute("""
    ALTER TABLE turno
      ADD CONSTRAINT turno_bar_fkey FOREIGN KEY (bar) REFERENCES bar(slug);
    """)

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
      t.audit_classification,
      b.rotulo AS bar_rotulo
    FROM turno t
    JOIN bar b ON b.slug = t.bar;
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
      ti.critical,
      b.rotulo AS bar_rotulo
    FROM turno t
    JOIN bar b ON b.slug = t.bar
    JOIN turno_item ti ON t.id = ti.turno_id
    WHERE ti.checked = FALSE
    ORDER BY t.date DESC, ti.critical DESC, ti.section_id;
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
      ta.pct,
      b.rotulo AS bar_rotulo
    FROM turno t
    JOIN bar b ON b.slug = t.bar
    JOIN turno_auditoria ta ON t.id = ta.turno_id
    ORDER BY t.date DESC, ta.criterio_id;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    # CREATE OR REPLACE VIEW não remove colunas: é preciso dropar e recriar
    # as views nas definições originais (sem bar_rotulo).
    op.execute("DROP VIEW IF EXISTS v_auditoria_detalhada;")
    op.execute("DROP VIEW IF EXISTS v_itens_faltantes;")
    op.execute("DROP VIEW IF EXISTS v_resumo_turno;")

    op.execute("""
    CREATE VIEW v_resumo_turno AS
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
    FROM turno t;
    """)

    op.execute("""
    CREATE VIEW v_itens_faltantes AS
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
    ORDER BY t.date DESC, ti.critical DESC, ti.section_id;
    """)

    op.execute("""
    CREATE VIEW v_auditoria_detalhada AS
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
    ORDER BY t.date DESC, ta.criterio_id;
    """)

    op.execute("ALTER TABLE turno DROP CONSTRAINT turno_bar_fkey;")
    op.execute("""
    ALTER TABLE turno
      ADD CONSTRAINT turno_bar_check CHECK (bar IN ('piscina', 'sport_bar'));
    """)
    op.execute("DROP TABLE IF EXISTS bar;")
