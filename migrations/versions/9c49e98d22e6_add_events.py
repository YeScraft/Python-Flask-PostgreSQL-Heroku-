"""add events

Revision ID: 9c49e98d22e6
Revises: 652339306099
Create Date: 2021-01-27 20:08:09.687797

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c49e98d22e6'
down_revision = '652339306099'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events',
    sa.Column('_id', sa.Integer(), nullable=False),
    sa.Column('author', sa.String(length=50), nullable=False),
    sa.Column('begin', sa.Date(), nullable=False),
    sa.Column('end', sa.Date(), nullable=False),
    sa.Column('topic', sa.String(length=80), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('events')
    # ### end Alembic commands ###
