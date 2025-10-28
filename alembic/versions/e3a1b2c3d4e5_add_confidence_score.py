"""
add confidence_score column to text_analyses

Revision ID: e3a1b2c3d4e5
Revises: 071540c71e08
Create Date: 2025-10-28
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3a1b2c3d4e5'
down_revision = '071540c71e08'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'text_analyses',
        sa.Column('confidence_score', sa.Float(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column('text_analyses', 'confidence_score')
