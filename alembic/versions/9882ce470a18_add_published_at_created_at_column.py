"""add published at created at column

Revision ID: 9882ce470a18
Revises: 8e5d98a315bd
Create Date: 2023-06-18 18:19:06.622327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9882ce470a18'
down_revision = '8e5d98a315bd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column("published",sa.Boolean(), server_default= 'TRUE', nullable = False))
    op.add_column('posts', sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
