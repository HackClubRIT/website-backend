"""create_users_table

Revision ID: 5c3f7ee9a2e4
Revises: 
Create Date: 2021-04-21 03:30:56.234309

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c3f7ee9a2e4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, auto_increment=True),
        sa.Column('username', sa.String, unique=True),
        sa.Column('password', sa.String),
        sa.Column('is_active', sa.Boolean, default=True)
    )


def downgrade():
    op.drop_table('users')
