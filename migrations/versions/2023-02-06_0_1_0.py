"""0.1.0

Revision ID: 52579d9625d8
Revises: 
Create Date: 2023-02-06 09:48:46.304731

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '52579d9625d8'
down_revision = None
branch_labels = None
depends_on = None


user_role_type = postgresql.ENUM('USER', 'ADMIN', name='user_role_type')
account_transaction_operation_type = postgresql.ENUM(
    'INCREMENT', 'DECREMENT', 'DECREMENT_SAFE', 'DECREMENT_ZERO', name='account_transaction_operation_type'
)
account_type = postgresql.ENUM('MAIN', name='account_type')


def upgrade() -> None:
    connection = op.get_bind()

    connection.execute("""CREATE EXTENSION IF NOT EXISTS "uuid-ossp";""")

    user_role_type.create(connection)
    account_transaction_operation_type.create(connection)
    account_type.create(connection)

    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('role', postgresql.ENUM(name='user_role_type', create_type=False), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('created_at', sa.Integer(), nullable=False),
        sa.Column('updated_at', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    op.create_table(
        'accounts',
        sa.Column('id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=True),
        sa.Column('balance', sa.BigInteger(), nullable=False),
        sa.Column('type', postgresql.ENUM(name='account_type', create_type=False), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'account_transactions',
        sa.Column('id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('pre_id', postgresql.UUID(), nullable=True),
        sa.Column('parent_id', postgresql.UUID(), nullable=True),
        sa.Column('account_id', postgresql.UUID(), nullable=True),
        sa.Column(
            'operation',
            postgresql.ENUM(name='account_transaction_operation_type', create_type=False),
            nullable=False
        ),
        sa.Column('size', sa.BigInteger(), nullable=False),
        sa.Column('balance', sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['parent_id'], ['account_transactions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['pre_id'], ['account_transactions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('pre_id')
    )
    op.create_index(
        'inx_open_account_unq',
        'account_transactions',
        ['pre_id', 'account_id'],
        unique=True,
        postgresql_where=sa.text('pre_id IS NULL')
    )


def downgrade() -> None:
    op.drop_index('inx_open_account_unq', table_name='account_transactions', postgresql_where=sa.text('pre_id IS NULL'))
    op.drop_table('account_transactions')
    op.drop_table('accounts')
    op.drop_table('users')

    connection = op.get_bind()
    user_role_type.drop(connection)
    account_transaction_operation_type.drop(connection)
    account_type.drop(connection)
