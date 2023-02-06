from src.app.user.enums import UserRoleType
from src.app.user.model import UserModel


async def save(
    name: str,
    username: str,
    email: str,
    password_hash: str
) -> UserModel:
    return await UserModel(
        name=name,
        username=username,
        email=email,
        password_hash=password_hash,
        role=UserRoleType.USER
    ).create()

