"""rename_column_username_on_users_table

Revision ID: 7ab423ce248e
Revises: c475fe148716
Create Date: 2021-04-30 04:26:43.289819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ab423ce248e'
down_revision = 'c475fe148716'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "users",
        "username",
        new_column_name="email"
    )


def downgrade():
    op.alter_column(
        "users",
        "email",
        new_column_name="username"
    )
