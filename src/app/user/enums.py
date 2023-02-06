import enum


class UserRoleType(str, enum.Enum):
    USER = 'USER',
    ADMIN = 'ADMIN',

