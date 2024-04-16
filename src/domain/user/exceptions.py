from qstd_core.exceptions import BadRequestException, BadRequestLocalizeException
from src.core.localization.enums import LocalizationKey


class UserWithThisEmailAlreadyExistsException(BadRequestException):
    message = 'User with this email already exists'
    code = 1000


class UserWithoutThisEmailAlreadyExistsLocalizationException(BadRequestLocalizeException):
    localization_key = LocalizationKey.USER_WITH_EMAIL_EXISTS
    code = 1001
