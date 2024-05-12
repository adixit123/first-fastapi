"""add published column

Revision ID: 6a7726a11ec0
Revises: a29c8af84e77
Create Date: 2024-05-12 22:20:38.302325

"""
from typing import Sequence, Union
from cgitb import text
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a7726a11ec0'
down_revision: Union[str, None] = 'a29c8af84e77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',sa.Column("published",sa.Boolean(),nullable=False,
                                    server_default='True'))
    
    op.add_column('posts',sa.Column("created_at",sa.TIMESTAMP(timezone=True),
                                    nullable=False,
                                    server_default=sa.text("now()")))
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
