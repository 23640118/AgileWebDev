"""empty message

Revision ID: 62cc664b0571
Revises: 57de0ce6db02
Create Date: 2024-05-19 02:20:33.926455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62cc664b0571'
down_revision = '57de0ce6db02'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.alter_column('rarity',
               existing_type=sa.TEXT(length=9),
               type_=sa.String(length=9),
               existing_nullable=True)
        batch_op.alter_column('name',
               existing_type=sa.TEXT(length=50),
               type_=sa.String(length=50),
               existing_nullable=True)
        batch_op.alter_column('artist',
               existing_type=sa.TEXT(length=50),
               type_=sa.String(length=50),
               existing_nullable=True)
        batch_op.alter_column('url',
               existing_type=sa.TEXT(length=100),
               type_=sa.String(length=100),
               existing_nullable=True)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('about', sa.String(length=500), nullable=True))

    with op.batch_alter_table('user_cards', schema=None) as batch_op:
        batch_op.add_column(sa.Column('obtain_date', sa.DateTime(timezone=True), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_cards', schema=None) as batch_op:
        batch_op.drop_column('obtain_date')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('about')

    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.alter_column('url',
               existing_type=sa.String(length=100),
               type_=sa.TEXT(length=100),
               existing_nullable=True)
        batch_op.alter_column('artist',
               existing_type=sa.String(length=50),
               type_=sa.TEXT(length=50),
               existing_nullable=True)
        batch_op.alter_column('name',
               existing_type=sa.String(length=50),
               type_=sa.TEXT(length=50),
               existing_nullable=True)
        batch_op.alter_column('rarity',
               existing_type=sa.String(length=9),
               type_=sa.TEXT(length=9),
               existing_nullable=True)

    # ### end Alembic commands ###