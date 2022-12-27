"""create_checks_table

Revision ID: 043c9891db35
Revises: 
Create Date: 2022-12-26 13:46:49.570233

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '043c9891db35'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "checks",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("site", sa.String(255), nullable=False),
        sa.Column("up", sa.BOOLEAN, nullable=True),
        sa.Column("downtime_reason", sa.String, nullable=True),
        sa.Column("response_duration", sa.Float, nullable=True),
        sa.Column("checked_at", sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("checks")
