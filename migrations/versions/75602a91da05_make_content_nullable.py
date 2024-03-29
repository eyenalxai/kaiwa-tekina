"""make content nullable

Revision ID: 75602a91da05
Revises: c4bf7b117147
Create Date: 2023-03-18 00:18:25.773487

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '75602a91da05'
down_revision = 'c4bf7b117147'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('message', 'content',
               existing_type=postgresql.BYTEA(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('message', 'content',
               existing_type=postgresql.BYTEA(),
               nullable=False)
    # ### end Alembic commands ###
