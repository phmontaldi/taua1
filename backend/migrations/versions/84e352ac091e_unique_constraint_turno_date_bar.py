"""unique constraint turno date bar

Revision ID: 84e352ac091e
Revises: 9763cbdb7bde
Create Date: 2026-07-08 21:55:21.071289

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '84e352ac091e'
down_revision: Union[str, Sequence[str], None] = '9763cbdb7bde'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TABLE turno ADD CONSTRAINT turno_date_bar_key UNIQUE (date, bar);")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TABLE turno DROP CONSTRAINT turno_date_bar_key;")
