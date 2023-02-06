from src.core.exception import BadRequestException


class UserWithEmailAlreadyExistsException(BadRequestException):
    message = 'A user with this email address exists'
    code = 1000

