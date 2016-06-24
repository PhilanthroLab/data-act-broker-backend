"""add_file_type_to_error

Revision ID: 78831b67d2b4
Revises: 926b0626182e
Create Date: 2016-06-23 19:53:25.468000

"""

# revision identifiers, used by Alembic.
revision = '78831b67d2b4'
down_revision = '18e9827a876d'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_error_data():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('error_metadata', sa.Column('file_type_id', sa.Integer(), nullable=True))
    op.add_column('error_metadata', sa.Column('target_file_type_id', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade_error_data():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('error_metadata', 'target_file_type_id')
    op.drop_column('error_metadata', 'file_type_id')
    ### end Alembic commands ###


def upgrade_job_tracker():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_job_tracker():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_user_manager():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_user_manager():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def upgrade_validation():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade_validation():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###

