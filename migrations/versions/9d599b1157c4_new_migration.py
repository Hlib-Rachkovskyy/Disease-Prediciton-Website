"""New migration

Revision ID: 9d599b1157c4
Revises: 664ec915027a
Create Date: 2024-06-26 21:57:25.649422

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d599b1157c4'
down_revision = '664ec915027a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('disease', schema=None) as batch_op:
        batch_op.alter_column('ListOfSymptoms',
               existing_type=sa.VARCHAR(length=377, collation='SQL_Latin1_General_CP1_CI_AS'),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('disease', schema=None) as batch_op:
        batch_op.alter_column('ListOfSymptoms',
               existing_type=sa.VARCHAR(length=377, collation='SQL_Latin1_General_CP1_CI_AS'),
               nullable=False)

    # ### end Alembic commands ###
