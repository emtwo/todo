"""Create ToDoList table

Revision ID: 2f1b61fbcf26
Revises: 
Create Date: 2021-02-08 18:49:00.039086

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f1b61fbcf26'
down_revision = None
branch_labels = None
depends_on = None



def upgrade():
	op.create_table("todolist",
	    sa.Column("id", sa.INTEGER(), autoincrement=True),
	    sa.Column("name", sa.String(length=50), nullable=False),
	    sa.Column("is_complete", sa.BOOLEAN(), nullable=True),
	    sa.PrimaryKeyConstraint('id', name='todolist_pkey'),
	    postgresql_ignore_search_path=False
    )
	op.create_table("task",
		sa.Column('id', sa.INTEGER(), autoincrement=True),
		sa.Column('title', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
		sa.Column('description', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
		sa.Column('status', sa.Enum('pending', 'done', name='status'), autoincrement=False, nullable=True),
		sa.Column('due_date', sa.TIMESTAMP(), autoincrement=False, nullable=True),
		sa.Column('list_id', sa.INTEGER(), autoincrement=False, nullable=True),
		sa.ForeignKeyConstraint(['list_id'], ['todolist.id'], name='task_list_id_fkey'),
		sa.PrimaryKeyConstraint('id', name='task_pkey')
    )


def downgrade():
    op.drop_table('todolist')
    op.drop_table('task')