"""create_table_feedback

Revision ID: 675d3ff81e17
Revises: 7ab423ce248e
Create Date: 2021-05-23 10:50:26.573440

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '675d3ff81e17'
down_revision = '7ab423ce248e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "feedbacks",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("content", sa.String),
        sa.Column("created_time", sa.DateTime, server_default=sa.func.now())
    )


def downgrade():
    op.drop_table("feedbacks")
