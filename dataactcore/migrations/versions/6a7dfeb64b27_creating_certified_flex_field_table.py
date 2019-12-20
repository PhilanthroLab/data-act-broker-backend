"""Creating certified_flex_field table

Revision ID: 6a7dfeb64b27
Revises: ee70a910db2e
Create Date: 2019-12-19 10:03:42.593857

"""

# revision identifiers, used by Alembic.
revision = '6a7dfeb64b27'
down_revision = 'ee70a910db2e'
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
    op.create_table('certified_flex_field',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('certified_flex_field_id', sa.Integer(), nullable=False),
    sa.Column('submission_id', sa.Integer(), nullable=False),
    sa.Column('job_id', sa.Integer(), nullable=True),
    sa.Column('row_number', sa.Integer(), nullable=True),
    sa.Column('header', sa.Text(), nullable=True),
    sa.Column('cell', sa.Text(), nullable=True),
    sa.Column('file_type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['submission_id'], ['submission.submission_id'], name='fk_certified_flex_field_submission_id', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('certified_flex_field_id')
    )
    op.create_index(op.f('ix_certified_flex_field_submission_id'), 'certified_flex_field', ['submission_id'], unique=False)
    # ### end Alembic commands ###


def downgrade_data_broker():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_certified_flex_field_submission_id'), table_name='certified_flex_field')
    op.drop_table('certified_flex_field')
    # ### end Alembic commands ###

