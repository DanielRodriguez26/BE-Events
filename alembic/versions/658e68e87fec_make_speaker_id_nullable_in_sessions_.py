"""Make speaker_id nullable in sessions table

Revision ID: 658e68e87fec
Revises: 7a2351cd2878
Create Date: 2025-08-22 23:36:20.944830

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "658e68e87fec"
down_revision = "7a2351cd2878"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Make speaker_id nullable in sessions table
    op.alter_column("sessions", "speaker_id", nullable=True)


def downgrade() -> None:
    # Make speaker_id not nullable in sessions table
    op.alter_column("sessions", "speaker_id", nullable=False)
