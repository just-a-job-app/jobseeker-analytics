"""add_celery_fields_to_taskruns

Revision ID: d357e1234567
Revises: c256d0279ea6
Create Date: 2025-06-30 15:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd357e1234567'
down_revision: Union[str, None] = 'c256d0279ea6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add celery_task_id and error_message columns to processing_task_runs table."""
    op.add_column('processing_task_runs', sa.Column('celery_task_id', sa.String(), nullable=True))
    op.add_column('processing_task_runs', sa.Column('error_message', sa.String(), nullable=True))


def downgrade() -> None:
    """Remove celery_task_id and error_message columns from processing_task_runs table."""
    op.drop_column('processing_task_runs', 'error_message')
    op.drop_column('processing_task_runs', 'celery_task_id')