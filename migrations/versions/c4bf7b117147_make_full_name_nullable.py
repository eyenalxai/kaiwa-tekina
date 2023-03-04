"""make full_name nullable

Revision ID: c4bf7b117147
Revises: c7c595c2f901
Create Date: 2023-03-03 23:27:39.578323

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'c4bf7b117147'
down_revision = 'c7c595c2f901'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'full_name',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'full_name',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    # ### end Alembic commands ###