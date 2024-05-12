"""add fkey to post

Revision ID: a29c8af84e77
Revises: d53415ddd0ee
Create Date: 2024-05-12 22:05:37.072825

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a29c8af84e77'
down_revision: Union[str, None] = 'd53415ddd0ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',sa.Column('user_id',
                                    sa.Integer,nullable=False))
    op.create_foreign_key('post_users_fk',source_table='posts',
                          referent_table='users',
                          local_cols=['user_id'],
                          remote_cols=['id'],
                          ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk',table_name="posts")
    op.drop_column('posts','user_id')
    pass
