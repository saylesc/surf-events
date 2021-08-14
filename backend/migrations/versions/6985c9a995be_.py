"""empty message

Revision ID: 6985c9a995be
Revises: 8d3446a3695e
Create Date: 2021-08-06 17:04:41.382574

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6985c9a995be'
down_revision = '8d3446a3695e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('SurfContest', sa.Column('contest_date', sa.DateTime(), nullable=False))
    op.add_column('SurfContest', sa.Column('contest_image', sa.String(length=500), nullable=True))
    op.add_column('SurfContest', sa.Column('contest_name', sa.String(), nullable=False))
    op.drop_column('SurfContest', 'contestDate')
    op.drop_column('SurfContest', 'contestName')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('SurfContest', sa.Column('contestName', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('SurfContest', sa.Column('contestDate', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_column('SurfContest', 'contest_name')
    op.drop_column('SurfContest', 'contest_image')
    op.drop_column('SurfContest', 'contest_date')
    # ### end Alembic commands ###
