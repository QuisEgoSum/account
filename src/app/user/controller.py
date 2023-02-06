from sanic import json

from src.app.user.schemas import RegistrationUser
from src.core import validator
from src.lib import openapi
from src.app.user import service


@openapi.tag('User')
@validator.body(RegistrationUser)
@openapi.response(RegistrationUser, status=201)
async def registration(request, body: RegistrationUser):
    """Registration"""
    return json(await service.registration(body), status=201)
