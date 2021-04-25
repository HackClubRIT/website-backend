"""add_column_role_to_users

Revision ID: 0979a70968e5
Revises: 5c3f7ee9a2e4
Create Date: 2021-04-23 06:57:44.570017

"""
from alembic import op
from sqlalchemy.dialects import postgresql
import sqlalchemy as sa
from app.users.roles import Roles

# revision identifiers, used by Alembic.
revision = '0979a70968e5'
down_revision = '5c3f7ee9a2e4'
branch_labels = None
depends_on = None


def upgrade():
    # Use sqlalchemy.dialects.mysql if using mysql
    roles = postgresql.ENUM(*[e.value for e in Roles], name="roles")
    roles.create(op.get_bind())

    op.add_column(
        "users",
        sa.Column("role", roles, nullable=False, default=Roles.USER.value, server_default=Roles.USER.value)
    )


def downgrade():
    op.drop_column("users", "role")
    sa.Enum(name='roles').drop(op.get_bind(), checkfirst=False)
