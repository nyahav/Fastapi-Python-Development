"""add content into post table

Revision ID: c3bb6e7cdbe8
Revises: 22da2e9a5f69
Create Date: 2024-10-31 18:50:05.042706

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3bb6e7cdbe8'
down_revision: Union[str, None] = '22da2e9a5f69'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass