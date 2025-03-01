"""create post table

Revision ID: 30365e8201c7
Revises: 
Create Date: 2025-02-26 11:57:07.449408

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '30365e8201c7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('tbl_post',
                    sa.Column('int_post_id',sa.Integer,primary_key=True,nullable=False),
                    sa.Column('vchr_title',sa.VARCHAR,nullable=False))


def downgrade() -> None:
    op.drop_table("tbl_post")
