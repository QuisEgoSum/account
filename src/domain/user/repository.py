from src.core.db import db

from src.domain.user.models import User


async def insert_user(user: dict):
    return await db.insert(User).values(user).returning(User.id, User.email, User.created_at).mapped_first()
