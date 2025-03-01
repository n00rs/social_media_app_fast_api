"""add user table

Revision ID: 52acdfb4b0db
Revises: c7b33bce7f2e
Create Date: 2025-02-26 23:59:49.636715

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52acdfb4b0db'
down_revision: Union[str, None] = 'c7b33bce7f2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("tbl_user",
                    sa.Column("int_user_id",sa.Integer,primary_key=  True,nullable= False),
                    sa.Column("vchr_email",sa.VARCHAR,nullable= False,unique= True),
                    sa.Column("vchr_password",sa.VARCHAR, nullable= False),
                    sa.Column("created_at",sa.TIMESTAMP(timezone= True),nullable= False,server_default=sa.text("now()"))
                    )


def downgrade() -> None:
    op.drop_table("tbl_user")
