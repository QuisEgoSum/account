from sanic import Sanic
from sanic.worker.loader import AppLoader
from sanic_cors import CORS
from src.app import routers
from src.core.config import config
from src.core import db
from src.lib.openapi import openapi_router
from src.server.http.modules.logger import logger_config
from src.server.http.modules.exception_handler import exception_handlers


async def start(_: Sanic):
    await db.connect()


async def shutdown(_: Sanic):
    await db.disconnect()


def create_http_server() -> Sanic:
    server = Sanic('HttpServer', log_config=logger_config)
    CORS(server)
    exception_handlers(server)
    server.blueprint(openapi_router)
    server.blueprint(routers)
    server.register_listener(start, 'after_server_start')
    server.register_listener(shutdown, 'before_server_stop')
    return server


def run():
    server_config = config.server.http
    loader = AppLoader(factory=create_http_server)
    server = loader.load()
    server.prepare(
        host=server_config.host,
        port=server_config.port,
        workers=server_config.workers,
        access_log=False
    )
    return Sanic.serve(primary=server, app_loader=loader)
