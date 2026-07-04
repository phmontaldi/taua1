"""initial schema

Revision ID: 9763cbdb7bde
Revises:
Create Date: 2026-07-04 18:38:58.311258

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '9763cbdb7bde'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
    CREATE EXTENSION IF NOT EXISTS "pgcrypto";
    """)

    op.execute("""
    CREATE TABLE turno (
      id                   UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
      date                 DATE         NOT NULL,
      bar                  VARCHAR(15)  NOT NULL CHECK (bar IN ('piscina', 'sport_bar')),
      emocionador          VARCHAR(100) NOT NULL,
      status               VARCHAR(50)  NOT NULL,
      submitted_at         TIMESTAMPTZ  NOT NULL,
      created_at           TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
      checklist_total      SMALLINT     NOT NULL,
      checklist_done       SMALLINT     NOT NULL,
      checklist_pct        NUMERIC(5,2) NOT NULL,
      critical_total       SMALLINT     NOT NULL,
      critical_done        SMALLINT     NOT NULL,
      critical_pct         NUMERIC(5,2) NOT NULL,
      audit_total          SMALLINT     NOT NULL,
      audit_pct            NUMERIC(5,2) NOT NULL,
      audit_classification VARCHAR(30)  NOT NULL
    );
    """)

    op.execute("""
    CREATE TABLE turno_item (
      id            UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
      turno_id      UUID         NOT NULL REFERENCES turno(id) ON DELETE CASCADE,
      item_id       VARCHAR(10)  NOT NULL,
      item_label    VARCHAR(200) NOT NULL,
      section_id    VARCHAR(5)   NOT NULL,
      section_title VARCHAR(100) NOT NULL,
      critical      BOOLEAN      NOT NULL DEFAULT FALSE,
      checked       BOOLEAN      NOT NULL DEFAULT FALSE
    );
    """)

    op.execute("""
    CREATE TABLE turno_auditoria (
      id             UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
      turno_id       UUID         NOT NULL REFERENCES turno(id) ON DELETE CASCADE,
      criterio_id    VARCHAR(5)   NOT NULL,
      criterio_label VARCHAR(200) NOT NULL,
      section_id     VARCHAR(2)   NOT NULL,
      section_title  VARCHAR(100) NOT NULL,
      score          SMALLINT     NOT NULL DEFAULT 0,
      max_score      SMALLINT     NOT NULL,
      pct            NUMERIC(5,2) GENERATED ALWAYS AS
                       (ROUND(score::NUMERIC / NULLIF(max_score,0) * 100, 2)) STORED
    );
    """)

    op.execute("CREATE INDEX idx_turno_date     ON turno(date);")
    op.execute("CREATE INDEX idx_turno_bar      ON turno(bar);")
    op.execute("CREATE INDEX idx_turno_date_bar ON turno(date, bar);")
    op.execute("CREATE INDEX idx_item_turno_id  ON turno_item(turno_id);")
    op.execute("CREATE INDEX idx_item_section   ON turno_item(section_id);")
    op.execute("CREATE INDEX idx_item_checked   ON turno_item(checked) WHERE checked = FALSE;")
    op.execute("CREATE INDEX idx_audit_turno_id ON turno_auditoria(turno_id);")
    op.execute("CREATE INDEX idx_audit_criterio ON turno_auditoria(criterio_id);")

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
    FROM turno t;
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
      ta.pct
    FROM turno t
    JOIN turno_auditoria ta ON t.id = ta.turno_id
    ORDER BY t.date DESC, ta.criterio_id;
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
    ORDER BY pct_falta DESC;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP VIEW IF EXISTS v_frequencia_falta_item;")
    op.execute("DROP VIEW IF EXISTS v_auditoria_detalhada;")
    op.execute("DROP VIEW IF EXISTS v_itens_faltantes;")
    op.execute("DROP VIEW IF EXISTS v_resumo_turno;")
    op.execute("DROP TABLE IF EXISTS turno_auditoria;")
    op.execute("DROP TABLE IF EXISTS turno_item;")
    op.execute("DROP TABLE IF EXISTS turno;")
