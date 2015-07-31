"""empty message

Revision ID: 4ad014956f76
Revises: 3bc40f8c5a68
Create Date: 2015-07-24 00:31:15.515140

"""

# revision identifiers, used by Alembic.
revision = '4ad014956f76'
down_revision = '3bc40f8c5a68'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('recommended_reads', sa.String(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'recommended_reads')
    ### end Alembic commands ###