"""add created_at and bln_published column

Revision ID: 86da2737baf5
Revises: 21897207d7f6
Create Date: 2025-02-28 00:00:13.283477

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86da2737baf5'
down_revision: Union[str, None] = '21897207d7f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("tbl_post",sa.Column("created_at",
                                       sa.TIMESTAMP(timezone=True),server_default= sa.text('now()'),nullable= False))
    op.add_column("tbl_post",sa.Column("bln_published",sa.Boolean,server_default='TRUE',nullable=False))


def downgrade() -> None:
    op.drop_column("tbl_post","created_at")
    op.drop_column("tbl_post","bln_published")
    
    
