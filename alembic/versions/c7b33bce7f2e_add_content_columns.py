"""add content columns

Revision ID: c7b33bce7f2e
Revises: 30365e8201c7
Create Date: 2025-02-26 12:17:33.346806

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7b33bce7f2e'
down_revision: Union[str, None] = '30365e8201c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("tbl_post",sa.Column("vchr_content",sa.VARCHAR,nullable=False))
    


def downgrade() -> None:
    op.drop_column("tbl_post","vchr_content")
