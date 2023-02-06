import bcrypt

from src.app.user.schemas import RegistrationUser
from src.app.user import repository
from src.app.user import exceptions
from src.app.account import service as account_service

from asyncpg.exceptions import UniqueViolationError

from src.core.db import db


async def registration(user: RegistrationUser):
    async with db.transaction():
        try:
            saved_user = await repository.save(
                user.name,
                user.email,
                user.username,
                bcrypt.hashpw(bytes(user.password, encoding='utf-8'), bcrypt.gensalt()).decode('utf-8')
            )
        except UniqueViolationError:
            raise exceptions.UserWithEmailAlreadyExistsException()
        await account_service.create_account(saved_user.id)
    return saved_user.to_dict()
