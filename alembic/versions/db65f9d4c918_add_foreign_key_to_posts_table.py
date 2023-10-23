"""add foreign-key to posts table

Revision ID: db65f9d4c918
Revises: 81dadafbda16
Create Date: 2023-10-24 02:46:05.569968

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db65f9d4c918'
down_revision: Union[str, None] = '81dadafbda16'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('id_user', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="user", local_cols=[
                          'id_user'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'id_user')
    pass
