"""Resync after missing migration

Revision ID: 45b3af1727dc
Revises: 45b6b7aee2eb
Create Date: 2025-07-07 16:43:45.916757

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '45b3af1727dc'
down_revision: Union[str, Sequence[str], None] = '45b6b7aee2eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('call', 'call_type',
               existing_type=postgresql.ENUM('inbound', 'outbound', name='calltype'),
               server_default=None,
               existing_nullable=False)
    op.alter_column('call', 'agent_environment',
               existing_type=postgresql.ENUM('production', 'development', name='agentenvironment'),
               server_default=None,
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('call', 'agent_environment',
               existing_type=postgresql.ENUM('production', 'development', name='agentenvironment'),
               server_default=sa.text("'production'::agentenvironment"),
               existing_nullable=False)
    op.alter_column('call', 'call_type',
               existing_type=postgresql.ENUM('inbound', 'outbound', name='calltype'),
               server_default=sa.text("'inbound'::calltype"),
               existing_nullable=False)
    # ### end Alembic commands ###
