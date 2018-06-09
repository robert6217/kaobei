"""empty message

Revision ID: ca2de204a65c
Revises: 
Create Date: 2018-06-01 11:37:00.861718

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca2de204a65c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('KaobeiID',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('FansPageID', sa.String(length=100), nullable=False),
    sa.Column('KaobeiName', sa.String(length=64), nullable=False),
    sa.Column('KaobeiPicture', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('ID'),
    sa.UniqueConstraint('FansPageID')
    )
    op.create_table('KaobeiData',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('PageID', sa.String(length=100), nullable=False),
    sa.Column('PostID', sa.String(length=200), nullable=False),
    sa.Column('PostTime', sa.DateTime(), nullable=False),
    sa.Column('PostMessage', sa.String(length=10000), nullable=True),
    sa.Column('PostLink', sa.String(length=50), nullable=True),
    sa.Column('PostLike', sa.Integer(), nullable=False),
    sa.Column('PostComment', sa.Integer(), nullable=False),
    sa.Column('PostShare', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['PageID'], ['KaobeiID.FansPageID'], ),
    sa.PrimaryKeyConstraint('ID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('KaobeiData')
    op.drop_table('KaobeiID')
    # ### end Alembic commands ###