"""add track details

Revision ID: 34c4ee3aec6b
Revises: d9f0475c4459
Create Date: 2022-10-01 15:58:45.558965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "34c4ee3aec6b"
down_revision = "d9f0475c4459"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "tracks",
        sa.Column("artist_name", sa.String(length=200), server_default=""),
    )
    op.add_column(
        "tracks",
        sa.Column("album_name", sa.String(length=100), server_default=""),
    )
    op.execute("UPDATE tracks SET artist_name = ''")
    op.execute("UPDATE tracks SET album_name = ''")

    op.alter_column("tracks", "artist_name", nullable=False)
    op.alter_column("tracks", "album_name", nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("tracks", "artist_name")
    # ### end Alembic commands ###