from sqlalchemy import insert

from src.app.account.enums import AccountType, AccountTransactionOperationType
from src.app.account.models import Account, AccountTransaction


async def insert_account(user_id: int, account_type: AccountType):
    return await insert(Account).values(user_id=user_id, type=account_type, balance=0)\
        .returning(Account.__table__)\
        .gino.first()


async def insert_open_transaction(account_id: int, balance: int):
    return await insert(AccountTransaction).values(
        account_id=account_id,
        balance=balance,
        type=AccountTransactionOperationType.INCREMENT,
        size=balance
    ).gino.status()
