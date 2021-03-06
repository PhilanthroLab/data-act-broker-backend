"""added external data load date

Revision ID: 9199891101c5
Revises: 321af67fae11
Create Date: 2018-06-05 10:35:23.538191

"""

# revision identifiers, used by Alembic.
revision = '9199891101c5'
down_revision = '321af67fae11'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_data_broker():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('external_data_type',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('external_data_type_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('external_data_type_id')
    )
    op.create_table('external_data_load_date',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('external_data_load_date_id', sa.Integer(), nullable=False),
    sa.Column('last_load_date', sa.Date(), nullable=True),
    sa.Column('external_data_type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['external_data_type_id'], ['external_data_type.external_data_type_id'], name='fk_external_data_type_id'),
    sa.PrimaryKeyConstraint('external_data_load_date_id'),
    sa.UniqueConstraint('external_data_type_id')
    )
    # ### end Alembic commands ###


def downgrade_data_broker():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('external_data_load_date')
    op.drop_table('external_data_type')
    # ### end Alembic commands ###

