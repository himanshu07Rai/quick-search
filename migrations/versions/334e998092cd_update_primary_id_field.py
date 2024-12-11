"""update primary id field

Revision ID: 334e998092cd
Revises: 978bf02ec468
Create Date: 2024-12-11 22:30:04.172121

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '334e998092cd'
down_revision: Union[str, None] = '978bf02ec468'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Drop the existing UUID column
    op.drop_column('posts', 'id')
    # Add a new auto-increment integer column
    op.add_column('posts', sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'id')
    op.add_column('posts', sa.Column('id', sa.dialects.postgresql.UUID(), primary_key=True))
    # ### end Alembic commands ###