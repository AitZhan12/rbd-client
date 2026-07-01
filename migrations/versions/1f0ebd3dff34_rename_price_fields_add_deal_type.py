"""rename price fields add deal_type

Revision ID: 1f0ebd3dff34
Revises: c877c86ce320
Create Date: 2026-06-29 18:52:54.366249

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1f0ebd3dff34'
down_revision: Union[str, Sequence[str], None] = 'c877c86ce320'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('apartments', sa.Column('deal_type', sa.Integer()))
    op.add_column('apartments', sa.Column('lease_price_period', sa.Integer()))


def downgrade() -> None:
    op.drop_column('apartments', 'deal_type')
    op.drop_column('apartments', 'lease_price_period')