"""add user fk in tbl_post

Revision ID: 21897207d7f6
Revises: 52acdfb4b0db
Create Date: 2025-02-27 23:39:05.740165

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '21897207d7f6'
down_revision: Union[str, None] = '52acdfb4b0db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("tbl_post",
                  sa.Column('int_user_id',sa.Integer,sa.ForeignKey(column="tbl_user.int_user_id",ondelete="CASCADE",name="tbl_post_tbl_user_int_user_id_fk")
                            ,nullable=False))
    # op.create_foreign_key("")


def downgrade() -> None:
    op.drop_constraint("tbl_post_tbl_user_int_user_id_fk","tbl_post")
    op.drop_column("tbl_post","int_user_id")
