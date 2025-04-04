"""add user ForeignKey in chat_history

Revision ID: 982c062f1a0c
Revises: a0e20d065e3c
Create Date: 2025-03-24 19:58:29.841421

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '982c062f1a0c'
down_revision: Union[str, None] = 'a0e20d065e3c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chat_history', sa.Column('chat_user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'chat_history', 'user', ['chat_user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'chat_history', type_='foreignkey')
    op.drop_column('chat_history', 'chat_user_id')
    # ### end Alembic commands ###
