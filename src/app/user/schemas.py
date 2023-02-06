from src.app.user.enums import UserRoleType
from src.core.validator import Schema
from pydantic import Field, constr


class RegistrationUser(Schema):
    name: str = Field(min_length=1, max_length=64)
    username: constr(min_length=1, max_length=32, to_lower=True)
    email: constr(min_length=3, max_length=256, to_lower=True)
    password: constr(min_length=6, max_length=128)
