"""Add TAS history fields

Revision ID: 4dc597500734
Revises: 885280875a1c
Create Date: 2016-10-26 19:37:17.347049

"""

# revision identifiers, used by Alembic.
revision = '4dc597500734'
down_revision = '885280875a1c'
branch_labels = None
depends_on = None

from datetime import date

from alembic import op
import sqlalchemy as sa


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()


# Helper table to make the data queries below a tad easier. We don't want to
# import TASLookup directly as its definition may change
tas_table = sa.Table(
    'tas_lookup',
    sa.MetaData(),
    sa.Column('tas_id', sa.Integer, primary_key=True),
    sa.Column('account_num', sa.Integer),
    sa.Column('internal_start_date', sa.Date)
)


def upgrade_data_broker():
    """We are moving some data around: moving all of the `tas_id` info into an
    `account_num` column, renumbering the `tas_id`, adding an two date columns
    and initializing one to 2015-01-01"""
    conn = op.get_bind()

    # Create the new columns, but all null. We'll fill them with data then set
    # them to be non-nullable
    op.add_column('tas_lookup',
                  sa.Column('account_num', sa.Integer(), nullable=True))
    op.add_column('tas_lookup',
                  sa.Column('internal_end_date', sa.Date(), nullable=True))
    op.add_column('tas_lookup',
                  sa.Column('internal_start_date', sa.Date(), nullable=True))

    # Set account_num to tas_id values
    conn.execute(tas_table.update().values(account_num=tas_table.c.tas_id))
    op.alter_column('tas_lookup', 'account_num', nullable=False)
    op.create_index(op.f('ix_tas_lookup_account_num'), 'tas_lookup',
                    ['account_num'], unique=False)

    # Reset tas_id values; we bump up all the existing tas_ids first to
    # prevent duplicates during the renumber
    max_tas_id = conn.execute(
        sa.sql.select([sa.func.max(tas_table.c.tas_id)])
    ).scalar() or 0
    conn.execute(
        tas_table.update().values(tas_id=tas_table.c.tas_id + max_tas_id))
    op.execute("ALTER SEQUENCE tas_lookup_tas_id_seq RESTART")
    op.execute("UPDATE tas_lookup SET tas_id = DEFAULT")
     
    # Finally, fill in the empty start dates with 2015-01-01, the beginning of
    # our accepted submissions
    conn.execute(
        tas_table.update().values(internal_start_date=date(2015, 1, 1)))
    op.alter_column('tas_lookup', 'internal_start_date', nullable=False)


def downgrade_data_broker():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tas_lookup', 'internal_start_date')
    op.drop_column('tas_lookup', 'internal_end_date')
    op.execute("UPDATE tas_lookup SET tas_id = account_num")
    op.drop_index(op.f('ix_tas_lookup_account_num'), table_name='tas_lookup')
    op.drop_column('tas_lookup', 'account_num')
    ### end Alembic commands ###

