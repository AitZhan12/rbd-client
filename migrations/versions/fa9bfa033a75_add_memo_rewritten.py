"""add memo_rewritten

Revision ID: fa9bfa033a75
Revises: 1f0ebd3dff34
Create Date: 2026-07-08 22:55:32.355812

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'fa9bfa033a75'
down_revision: Union[str, Sequence[str], None] = '1f0ebd3dff34'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('apartments', sa.Column('memo_rewritten', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('apartments', 'memo_rewritten')