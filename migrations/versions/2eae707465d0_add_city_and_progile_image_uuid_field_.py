"""add city and progile_image_uuid field tp prganization table

Revision ID: 2eae707465d0
Revises: 48f861c5dc00
Create Date: 2023-06-18 18:27:19.448235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2eae707465d0'
down_revision = '48f861c5dc00'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('organization', schema=None) as batch_op:
        batch_op.add_column(sa.Column('city', sa.Text(), nullable=False))
        batch_op.add_column(sa.Column('profile_image_uuid', sa.String(length=100), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('organization', schema=None) as batch_op:
        batch_op.drop_column('profile_image_uuid')
        batch_op.drop_column('city')

    # ### end Alembic commands ###
