"""add column content to posts table

Revision ID: 59a3ab9b7e0a
Revises: 8a2cfc8248ab
Create Date: 2023-10-24 02:39:32.853938

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '59a3ab9b7e0a'
down_revision: Union[str, None] = '8a2cfc8248ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
