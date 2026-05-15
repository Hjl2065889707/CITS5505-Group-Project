"""add is_deleted to posts

Revision ID: a8f2c4d9b731
Revises: 5168a835ed43
Create Date: 2026-05-15 21:10:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8f2c4d9b731'
down_revision = '5168a835ed43'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column(
            'is_deleted',
            sa.Boolean(),
            server_default=sa.false(),
            nullable=False,
        ),
    )


def downgrade():
    op.drop_column('posts', 'is_deleted')
