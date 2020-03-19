"""empty message

Revision ID: 3b77f6412fdd
Revises: 
Create Date: 2019-08-24 13:37:35.862114

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b77f6412fdd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('enname', sa.String(length=80), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_time', sa.DateTime(), nullable=False),
    sa.Column('updated_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('enname'),
    sa.UniqueConstraint('name')
    )
    op.create_table('menu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('en_name', sa.String(length=80), nullable=False),
    sa.Column('fid', sa.Integer(), nullable=True),
    sa.Column('url', sa.String(length=500), nullable=False),
    sa.Column('component', sa.String(length=500), nullable=False),
    sa.Column('icon', sa.String(length=50), nullable=True),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('type', sa.Integer(), nullable=False),
    sa.Column('order', sa.Integer(), nullable=False),
    sa.Column('created_time', sa.DateTime(), nullable=False),
    sa.Column('updated_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('component'),
    sa.UniqueConstraint('en_name'),
    sa.UniqueConstraint('icon'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('url')
    )
    op.create_table('position',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('enname', sa.String(length=80), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_time', sa.DateTime(), nullable=False),
    sa.Column('updated_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('enname'),
    sa.UniqueConstraint('name')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('enname', sa.String(length=80), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('created_time', sa.DateTime(), nullable=False),
    sa.Column('updated_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('enname'),
    sa.UniqueConstraint('name')
    )
    op.create_table('tmenu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('fid', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('role_menu',
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('menu_id', sa.Integer(), nullable=False),
    sa.Column('created_time', sa.DateTime(), nullable=False),
    sa.Column('updated_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['menu_id'], ['menu.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('role_id', 'menu_id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=120), nullable=False),
    sa.Column('gender', sa.Integer(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('position_id', sa.Integer(), nullable=False),
    sa.Column('created_time', sa.DateTime(), nullable=False),
    sa.Column('updated_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.ForeignKeyConstraint(['position_id'], ['position.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('user_role',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('created_time', sa.DateTime(), nullable=False),
    sa.Column('updated_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'role_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_role')
    op.drop_table('user')
    op.drop_table('role_menu')
    op.drop_table('tmenu')
    op.drop_table('role')
    op.drop_table('position')
    op.drop_table('menu')
    op.drop_table('group')
    # ### end Alembic commands ###
