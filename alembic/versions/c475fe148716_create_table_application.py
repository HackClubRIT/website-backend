"""create_table_application

Revision ID: c475fe148716
Revises: 0979a70968e5
Create Date: 2021-04-27 14:12:23.945564

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from app.applications.application_states import ApplicationStates

revision = 'c475fe148716'
down_revision = '0979a70968e5'
branch_labels = None
depends_on = None


def upgrade():
    # TODO replace string with Enum
    # Use sqlalchemy.dialects.mysql if using mysql
    #app_status = postgresql.ENUM(*[e.value for e in ApplicationStates], name="app_status")
    #app_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "applications",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String, nullable=False),
        sa.Column("created_date", sa.DateTime, server_default=sa.func.now()),
        sa.Column("data", sa.JSON, nullable=False),
        sa.Column("status", sa.String, default=ApplicationStates.PENDING.value, server_default=ApplicationStates.PENDING.value)
    )


def downgrade():
    #op.drop_table("applications")
    sa.Enum(name='app_status').drop(op.get_bind(), checkfirst=False)
