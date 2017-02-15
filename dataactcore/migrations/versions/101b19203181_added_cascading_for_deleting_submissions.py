"""Added cascading for deleting submissions

Revision ID: 101b19203181
Revises: 88e9b634ca1a
Create Date: 2017-02-15 15:25:09.518566

"""

# revision identifiers, used by Alembic.
revision = '101b19203181'
down_revision = '88e9b634ca1a'
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
    op.create_foreign_key('fk_appropriation_submission_id', 'appropriation', 'submission', ['submission_id'], ['submission_id'], ondelete='CASCADE')
    op.create_foreign_key('fk_award_financial_submission_id', 'award_financial', 'submission', ['submission_id'], ['submission_id'], ondelete='CASCADE')
    op.create_foreign_key('fk_award_financial_assistance_submission_id', 'award_financial_assistance', 'submission', ['submission_id'], ['submission_id'], ondelete='CASCADE')
    op.create_foreign_key('fk_award_procurement_submission_id', 'award_procurement', 'submission', ['submission_id'], ['submission_id'], ondelete='CASCADE')
    op.create_foreign_key('fk_error_metadata_job', 'error_metadata', 'job', ['job_id'], ['job_id'], ondelete='CASCADE')
    op.create_foreign_key('fk_file_job', 'file', 'job', ['job_id'], ['job_id'], ondelete='CASCADE')
    op.drop_constraint('fk_generation_job', 'file_generation_task', type_='foreignkey')
    op.create_foreign_key('fk_generation_job', 'file_generation_task', 'job', ['job_id'], ['job_id'], ondelete='CASCADE')
    op.create_foreign_key('fk_flex_field_submission_id', 'flex_field', 'submission', ['submission_id'], ['submission_id'], ondelete='CASCADE')
    op.drop_constraint('fk_prereq_job_id', 'job_dependency', type_='foreignkey')
    op.drop_constraint('fk_dep_job_id', 'job_dependency', type_='foreignkey')
    op.create_foreign_key('fk_dep_job_id', 'job_dependency', 'job', ['job_id'], ['job_id'], ondelete='CASCADE')
    op.create_foreign_key('fk_prereq_job_id', 'job_dependency', 'job', ['prerequisite_id'], ['job_id'], ondelete='CASCADE')
    op.create_foreign_key('fk_object_class_program_activity_submission_id', 'object_class_program_activity', 'submission', ['submission_id'], ['submission_id'], ondelete='CASCADE')
    op.drop_constraint('fk_submission', 'submission_narrative', type_='foreignkey')
    op.create_foreign_key('fk_submission', 'submission_narrative', 'submission', ['submission_id'], ['submission_id'], ondelete='CASCADE')
    ### end Alembic commands ###


def downgrade_data_broker():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_submission', 'submission_narrative', type_='foreignkey')
    op.create_foreign_key('fk_submission', 'submission_narrative', 'submission', ['submission_id'], ['submission_id'])
    op.drop_constraint('fk_object_class_program_activity_submission_id', 'object_class_program_activity', type_='foreignkey')
    op.drop_constraint('fk_prereq_job_id', 'job_dependency', type_='foreignkey')
    op.drop_constraint('fk_dep_job_id', 'job_dependency', type_='foreignkey')
    op.create_foreign_key('fk_dep_job_id', 'job_dependency', 'job', ['job_id'], ['job_id'])
    op.create_foreign_key('fk_prereq_job_id', 'job_dependency', 'job', ['prerequisite_id'], ['job_id'])
    op.drop_constraint('fk_flex_field_submission_id', 'flex_field', type_='foreignkey')
    op.drop_constraint('fk_generation_job', 'file_generation_task', type_='foreignkey')
    op.create_foreign_key('fk_generation_job', 'file_generation_task', 'job', ['job_id'], ['job_id'])
    op.drop_constraint('fk_file_job', 'file', type_='foreignkey')
    op.drop_constraint('fk_error_metadata_job', 'error_metadata', type_='foreignkey')
    op.drop_constraint('fk_award_procurement_submission_id', 'award_procurement', type_='foreignkey')
    op.drop_constraint('fk_award_financial_assistance_submission_id', 'award_financial_assistance', type_='foreignkey')
    op.drop_constraint('fk_award_financial_submission_id', 'award_financial', type_='foreignkey')
    op.drop_constraint('fk_appropriation_submission_id', 'appropriation', type_='foreignkey')
    ### end Alembic commands ###

