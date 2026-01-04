"""initial_schema

Revision ID: e7ea238b7760
Revises: 
Create Date: 2025-11-19 17:44:07.285754

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'e7ea238b7760'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Get the database connection
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = inspector.get_table_names()
    # adding "if" statements to make this crash proof in prod. 
    # migration history is corrupted because I didn't know how to use alembic :)
    if 'companies' not in existing_tables:
        op.create_table('companies',
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.Column('company_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('company_email_domain', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint('company_id'),
        sa.UniqueConstraint('company_name', 'company_email_domain', name='unique_company_name_and_domain')
        )
    if 'user_emails' not in existing_tables:
        op.create_table('user_emails',
        sa.Column('id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('user_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('company_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('application_status', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('received_at', sa.DateTime(), nullable=False),
        sa.Column('subject', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('job_title', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('normalized_job_title', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('email_from', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint('id', 'user_id')
        )
    if 'users' not in existing_tables:
        op.create_table('users',
        sa.Column('user_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('user_email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('start_date', sa.DateTime(), nullable=True),
        sa.Column('role', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint('user_id')
        )
    if 'processing_task_runs' not in existing_tables:
        op.create_table('processing_task_runs',
        sa.Column('user_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('created', sa.DateTime(), nullable=False),
        sa.Column('updated', sa.DateTime(), nullable=False),
        sa.Column('status', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('total_emails', sa.Integer(), nullable=False),
        sa.Column('processed_emails', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
        sa.PrimaryKeyConstraint('user_id')
        )
    if 'coach_client_link' not in existing_tables:
        op.create_table('coach_client_link',
        sa.Column('coach_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('client_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('start_date', sa.DateTime(), nullable=False),
        sa.Column('end_date', sa.DateTime(), nullable=True),
        sa.Column('created', sa.DateTime(), nullable=False),
        sa.Column('updated', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['client_id'], ['users.user_id'], ),
        sa.ForeignKeyConstraint(['coach_id'], ['users.user_id'], ),
        sa.PrimaryKeyConstraint('coach_id', 'client_id')
        )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # dont want to drop existing prod tables
    op.drop_table('coach_client_link')

    # ### end Alembic commands ###
