"""create poss table

Revision ID: 56ea979fbc94
Revises: 
Create Date: 2023-06-18 17:30:58.958327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56ea979fbc94'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id',sa.Integer(), primary_key = True, nullable = False),
                     sa.Column("title", sa.String(), nullable = False))
    pass
    
def downgrade() -> None:
    op.drop_table('posts')
    pass
