"""create_table_events

Revision ID: 0ca33b933838
Revises: 675d3ff81e17
Create Date: 2021-06-03 19:25:00.786381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ca33b933838'
down_revision = '03f880864a08'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "events",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("description", sa.String, nullable=False),
        sa.Column("date", sa.DateTime, nullable=False),
        sa.Column("image_id", sa.Integer, sa.ForeignKey("images.id"), nullable=False),
        sa.Column("registration_link", sa.String, nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
    )


def downgrade():
    op.drop_table("events")
