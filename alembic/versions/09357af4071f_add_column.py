"""add column

Revision ID: 09357af4071f
Revises: e144ef4c5dc4
Create Date: 2024-05-12 21:04:53.401778

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '09357af4071f'
down_revision: Union[str, None] = 'e144ef4c5dc4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() :
    op.drop_column('posts','content')
    pass
