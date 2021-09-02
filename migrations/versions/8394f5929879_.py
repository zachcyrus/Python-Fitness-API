"""empty message

Revision ID: 8394f5929879
Revises: f95b3a14d71e
Create Date: 2021-08-25 14:39:29.614982

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8394f5929879'
down_revision = 'f95b3a14d71e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('routines',
    sa.Column('routine_id', sa.Integer(), nullable=False),
    sa.Column('routine_name', sa.String(length=50), nullable=False),
    sa.Column('routine_description', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('routine_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('routines')
    # ### end Alembic commands ###