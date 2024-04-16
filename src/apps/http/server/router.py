from sanic import Blueprint

from qstd_core.openapi import openapi_router
from src.apps.http.app.user.router import user_router
from src.core.sanic.openapi import docs_router

router = Blueprint.group(
    docs_router,
    openapi_router,
    user_router
)
