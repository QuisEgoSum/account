import bcrypt
from sqlalchemy.exc import IntegrityError

from src.domain.user import exceptions, repository, dto


async def register_user(user: dict):
    try:
        saved_user = await repository.insert_user(
            dict(
                email=user['email'],
                password_hash=bcrypt.hashpw(
                    bytes(user['password'], encoding='utf-8'), bcrypt.gensalt()
                ).decode('utf-8')
            )
        )
        return dict(**saved_user)
    except IntegrityError:
        raise exceptions.UserWithThisEmailAlreadyExistsException()


async def register_user_v2(user: dto.RegisterUserDto):
    try:
        saved_user = await repository.insert_user(
            dict(
                email=user.email,
                password_hash=bcrypt.hashpw(
                    bytes(user.password, encoding='utf-8'), bcrypt.gensalt()
                ).decode('utf-8')
            )
        )
        return dict(**saved_user)
    except IntegrityError:
        raise exceptions.UserWithoutThisEmailAlreadyExistsLocalizationException()
