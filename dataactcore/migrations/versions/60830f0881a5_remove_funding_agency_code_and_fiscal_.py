"""Remove funding_agency_code and fiscal_year_and_quarter_correction from DetachedAwardProcurement

Revision ID: 60830f0881a5
Revises: 654507a3934c
Create Date: 2018-03-09 08:34:01.278504

"""

# revision identifiers, used by Alembic.
revision = '60830f0881a5'
down_revision = '654507a3934c'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_data_broker():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('detached_award_financial_assistance', 'fiscal_year_and_quarter_co')
    op.drop_column('detached_award_financial_assistance', 'funding_agency_code')
    ### end Alembic commands ###


def downgrade_data_broker():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('detached_award_financial_assistance', sa.Column('funding_agency_code', sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column('detached_award_financial_assistance', sa.Column('fiscal_year_and_quarter_co', sa.TEXT(), autoincrement=False, nullable=True))
    ### end Alembic commands ###

