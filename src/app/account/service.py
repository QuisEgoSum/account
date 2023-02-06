from src.app.account.enums import AccountType
from src.core.db import db
from src.app.account import repository


async def create_account(user_id: int):
    async with db.transaction():
        account = await repository.insert_account(user_id, AccountType.MAIN)
        await repository.insert_open_transaction(account.id, account.balance)

