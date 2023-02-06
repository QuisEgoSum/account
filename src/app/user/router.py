from sanic import Blueprint
from src.app.user import controller


user_router = Blueprint('User')


user_router.add_route(uri='/registration', methods=['POST'], handler=controller.registration)
