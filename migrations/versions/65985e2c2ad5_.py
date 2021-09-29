"""empty message

Revision ID: 65985e2c2ad5
Revises: a8f3fde7823d
Create Date: 2021-09-29 12:44:46.617036

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65985e2c2ad5'
down_revision = 'a8f3fde7823d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('logs', sa.Column('routine_exercise_id', sa.Integer(), nullable=True))
    op.drop_constraint('logs_personal_routine_id_fkey', 'logs', type_='foreignkey')
    op.create_foreign_key(None, 'logs', 'routine_exercises', ['routine_exercise_id'], ['routine_exercise_id'])
    op.drop_column('logs', 'personal_routine_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('logs', sa.Column('personal_routine_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'logs', type_='foreignkey')
    op.create_foreign_key('logs_personal_routine_id_fkey', 'logs', 'user_routine_exercises', ['personal_routine_id'], ['personal_routine_exercise_id'])
    op.drop_column('logs', 'routine_exercise_id')
    # ### end Alembic commands ###
