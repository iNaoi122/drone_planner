"""Add initila data

Revision ID: 85fed3cbaa65
Revises: c72316dbd8c3
Create Date: 2025-06-15 12:14:50.174193

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid
from passlib.context import CryptContext
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '85fed3cbaa65'
down_revision: Union[str, None] = 'c72316dbd8c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def upgrade() -> None:
    """Upgrade schema."""
    roles_table = sa.table(
        'role',
        sa.column('id', UUID(as_uuid=True)),
        sa.column('title', sa.String(50)),
        sa.column('created_at', sa.DateTime())
    )

    users_table = sa.table(
        'user',
        sa.column('id', UUID(as_uuid=True)),
        sa.column('first_name', sa.String(255)),
        sa.column('last_name', sa.String(255)),
        sa.column('middle_name', sa.String(255)),
        sa.column('age', sa.Integer()),
        sa.column('login', sa.String(255)),
        sa.column('password', sa.String(255)),
        sa.column('role_id', UUID(as_uuid=True)),
        sa.column('id_card_series', sa.Integer()),
        sa.column('id_card_number', sa.Integer()),
        sa.column('created_at', sa.DateTime())
    )

    op.bulk_insert(roles_table, [
        {'id': uuid.uuid4(), 'title': 'admin', 'created_at': datetime.utcnow()},
        {'id': uuid.uuid4(), 'title': 'user', 'created_at': datetime.utcnow()},
    ])

    connection = op.get_bind()
    admin_role_id = connection.execute(
        sa.select(roles_table.c.id).where(roles_table.c.title == 'admin')
    ).scalar()

    user_role_id = connection.execute(
        sa.select(roles_table.c.id).where(roles_table.c.title == 'user')
    ).scalar()

    op.bulk_insert(users_table, [
        {
            'id': uuid.uuid4(),
            'first_name': 'Иванов',
            'last_name': 'Иван',
            'middle_name': 'Иванович',
            'age':30,
            'login': 'admin',
            'password': pwd_context.hash('secret'),
            'role_id': admin_role_id,
            'id_card_series':1234,
            'id_card_number':5678,
            'created_at': datetime.utcnow()
        },
        {
            'id': uuid.uuid4(),
            'first_name': 'Пользователь',
            'last_name': 'Пользователь',
            'middle_name': 'Пользович',
            'age':20,
            'login': 'user',
            'password': pwd_context.hash('secret'),
            'role_id': user_role_id,
            'id_card_series': 1234,
            'id_card_number': 5678,
            'created_at': datetime.utcnow()
        }
    ])

    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
