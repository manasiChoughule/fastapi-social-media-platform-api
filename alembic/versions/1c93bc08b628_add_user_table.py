"""add user table

Revision ID: 1c93bc08b628
Revises: 59410cd055b1
Create Date: 2023-06-18 18:03:54.542721

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c93bc08b628'
down_revision = '59410cd055b1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column("id",sa.Integer(), primary_key = True, nullable = False),
                    sa.Column("email", sa.String(), nullable=False, unique = True),
                    sa.Column("password",sa.String(), nullable=False),
                    sa.Column("created_at",sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
                    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
