"""add content column to posts table

Revision ID: 59410cd055b1
Revises: 56ea979fbc94
Create Date: 2023-06-18 18:00:06.073524

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59410cd055b1'
down_revision = '56ea979fbc94'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
