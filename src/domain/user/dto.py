from pydantic import BaseModel


class RegisterUserDto(BaseModel):
    email: str
    password: str
