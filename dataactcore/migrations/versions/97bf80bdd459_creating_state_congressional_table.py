"""Creating state_congressional table

Revision ID: 97bf80bdd459
Revises: 9960bbbe4d92
Create Date: 2017-09-08 14:34:57.783817

"""

# revision identifiers, used by Alembic.
revision = '97bf80bdd459'
down_revision = '9960bbbe4d92'
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
    op.create_table('state_congressional',
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('state_congressional_id', sa.Integer(), nullable=False),
        sa.Column('state_code', sa.Text(), nullable=True),
        sa.Column('congressional_district_no', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('state_congressional_id')
    )
    op.create_index('ix_sc_state_cd', 'state_congressional', ['state_code', 'congressional_district_no'], unique=True)
    op.create_index(op.f('ix_state_congressional_congressional_district_no'), 'state_congressional', ['congressional_district_no'], unique=False)
    op.create_index(op.f('ix_state_congressional_state_code'), 'state_congressional', ['state_code'], unique=False)
    op.execute("""
            INSERT INTO state_congressional (created_at, updated_at, state_code, congressional_district_no)
            SELECT DISTINCT NOW(), NOW(), state_abbreviation, congressional_district_no
            FROM zips
            ORDER BY state_abbreviation, congressional_district_no
        """)
    ### end Alembic commands ###


def downgrade_data_broker():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_state_congressional_state_code'), table_name='state_congressional')
    op.drop_index(op.f('ix_state_congressional_congressional_district_no'), table_name='state_congressional')
    op.drop_index('ix_sc_state_cd', table_name='state_congressional')
    op.drop_table('state_congressional')
    ### end Alembic commands ###

