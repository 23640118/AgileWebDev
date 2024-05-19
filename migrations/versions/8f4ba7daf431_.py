"""empty message

Revision ID: 8f4ba7daf431
Revises: 62cc664b0571
Create Date: 2024-05-19 13:39:01.918261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f4ba7daf431'
down_revision = '62cc664b0571'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_cards', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantity', sa.Integer(), nullable=True))
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('card_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_column('obtain_date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_cards', schema=None) as batch_op:
        batch_op.add_column(sa.Column('obtain_date', sa.DATETIME(), nullable=True))
        batch_op.alter_column('card_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.drop_column('quantity')

    # ### end Alembic commands ###