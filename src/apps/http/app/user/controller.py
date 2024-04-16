from sanic import Request, response

from qstd_core import openapi, validator
from src.domain.user import service, schemas, dto, exceptions


@openapi.tag('User')
@openapi.errors(exceptions.UserWithThisEmailAlreadyExistsException)
@validator.body(schemas.RegisterSchema())
async def register(_: Request, body: dict):
    """
    Register a new user
    """
    return response.json(await service.register_user(body))


@openapi.tag('User')
@openapi.errors(exceptions.UserWithoutThisEmailAlreadyExistsLocalizationException)
@validator.body(dto.RegisterUserDto)
async def register_v2(_: Request, body: dto.RegisterUserDto):
    """
    Register a new user v2
    """
    return response.json(await service.register_user_v2(body))
