"""empty message

Revision ID: 57de0ce6db02
Revises: ada689a4eeb2
Create Date: 2024-05-13 16:31:54.441421

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57de0ce6db02'
down_revision = 'ada689a4eeb2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.add_column(sa.Column('artist', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('year', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.drop_column('year')
        batch_op.drop_column('artist')

    # ### end Alembic commands ###
