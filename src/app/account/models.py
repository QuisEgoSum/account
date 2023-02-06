from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy import text

from src.app.account.enums import AccountTransactionOperationType, AccountType
from src.core.db import db


class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(UUID(), primary_key=True, server_default=text("uuid_generate_v4()"))
    user_id = db.Column(db.BigInteger(), db.ForeignKey('users.id', ondelete='CASCADE'))
    balance = db.Column(db.BigInteger(), nullable=False)
    type = db.Column(ENUM(AccountType, name='account_type'), nullable=False)


class AccountTransaction(db.Model):
    __tablename__ = 'account_transactions'

    id = db.Column(UUID(), primary_key=True, server_default=text("uuid_generate_v4()"))
    pre_id = db.Column(UUID(), db.ForeignKey('account_transactions.id', ondelete='CASCADE'), unique=True)
    parent_id = db.Column(UUID(), db.ForeignKey('account_transactions.id', ondelete='CASCADE'))
    account_id = db.Column(UUID(), db.ForeignKey('accounts.id', ondelete='CASCADE'))
    operation = db.Column(
        ENUM(AccountTransactionOperationType, name='account_transaction_operation_type'), nullable=False
    )
    size = db.Column(db.BigInteger(), nullable=False)
    balance = db.Column(db.BigInteger(), nullable=False)

    inx_open_account_unq = db.Index(
        'inx_open_account_unq',
        pre_id,
        account_id,
        postgresql_where=pre_id.is_(None),
        unique=True
    )
