"""create_images_table

Revision ID: 03f880864a08
Revises: 0ca33b933838
Create Date: 2021-06-06 16:27:45.820728

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03f880864a08'
down_revision = '675d3ff81e17'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "images",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("url", sa.String, nullable=False)
    )


def downgrade():
    op.drop_table("events")
