"""initial 2

Revision ID: fbb425aa40b6
Revises: 5d4fa87722a3
Create Date: 2023-03-03 19:17:01.481616

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbb425aa40b6'
down_revision = '5d4fa87722a3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('content', sa.String(length=4096), nullable=False))
    op.drop_column('message', 'text')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('text', sa.VARCHAR(length=4096), autoincrement=False, nullable=False))
    op.drop_column('message', 'content')
    # ### end Alembic commands ###
