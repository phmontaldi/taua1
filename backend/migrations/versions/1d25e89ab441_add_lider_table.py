"""add lider table

Revision ID: 1d25e89ab441
Revises: 84e352ac091e
Create Date: 2026-07-08 22:30:00.000000

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '1d25e89ab441'
down_revision: Union[str, Sequence[str], None] = '84e352ac091e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
    CREATE TABLE lider (
      id         UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
      nome       VARCHAR(100) NOT NULL UNIQUE,
      pin_hash   VARCHAR(255) NOT NULL,
      ativo      BOOLEAN      NOT NULL DEFAULT TRUE,
      created_at TIMESTAMPTZ  NOT NULL DEFAULT NOW()
    );
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE IF EXISTS lider;")
