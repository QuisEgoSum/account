from sqlalchemy.dialects.postgresql import ENUM

from src.app.user.enums import UserRoleType
from src.core.db import db, TimestampedModel


class UserModel(TimestampedModel):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    role = db.Column(ENUM(UserRoleType, name='user_role_type'), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
