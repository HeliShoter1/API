"""add last few column to posts table

Revision ID: 27af291c0e9f
Revises: db65f9d4c918
Create Date: 2023-10-24 02:55:49.866957

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27af291c0e9f'
down_revision: Union[str, None] = 'db65f9d4c918'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column(
        'rating', sa.Integer, nullable=False,))
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts', 'rating')
    op.drop_column('posts', 'created_at')
    pass
