"""Added client model

Revision ID: c8cc96fe019a
Revises: 89fb2f20918d
Create Date: 2023-12-12 12:59:01.842945

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c8cc96fe019a'
down_revision: Union[str, None] = '89fb2f20918d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clients',
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('client_name', sa.String(length=25), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('contact_number', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('client_id'),
    sa.UniqueConstraint('email', name='unique_email')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('clients')
    # ### end Alembic commands ###
