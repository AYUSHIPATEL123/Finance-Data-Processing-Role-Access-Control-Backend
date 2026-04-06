"""remove unique constrain from passwor sin users

Revision ID: 599412335eec
Revises: f18470271cb8
Create Date: 2026-04-06 21:08:11.560495

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '599412335eec'
down_revision: Union[str, Sequence[str], None] = 'f18470271cb8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint('password','users',type_='unique')


def downgrade() -> None:
    """Downgrade schema."""
    op.create_unique_constraint('password','users',['password'])
