"""Add capacity field to sessions table

Revision ID: 7a2351cd2878
Revises: c2442b5a4719
Create Date: 2025-08-22 23:32:09.310815

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "7a2351cd2878"
down_revision = "c2442b5a4719"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add capacity column to sessions table
    op.add_column("sessions", sa.Column("capacity", sa.Integer(), nullable=True))


def downgrade() -> None:
    # Remove capacity column from sessions table
    op.drop_column("sessions", "capacity")
