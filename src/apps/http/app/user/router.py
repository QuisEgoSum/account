from sanic import Blueprint
from . import controller

user_router = Blueprint('user')

user_router.add_route(controller.register, '/user/register', ['POST'])
user_router.add_route(controller.register_v2, '/v2/user/register', ['POST'])
