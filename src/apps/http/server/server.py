import asyncio

from sanic import Sanic
from sanic.worker.loader import AppLoader

import qstd_core.sanic.server.utils
from src import core
from src.core.config import config, manager as config_manager
from src.core.logger import app_logger

from .router import router

logger = app_logger.getChild(__name__)


async def start(app: Sanic, _: asyncio.AbstractEventLoop):
    config_manager.set_multiprocessing_config_dict(app.shared_ctx.config)


async def do_start(_: Sanic, __: asyncio.AbstractEventLoop):
    logger.info("Server successfully started")


async def shutdown(_: Sanic, __: asyncio.AbstractEventLoop):
    logger.info("Server shutting down")


async def do_shutdown(_: Sanic, __: asyncio.AbstractEventLoop):
    logger.info("Server successfully stopped")


def create_http_server():
    server = Sanic("HTTP", configure_logging=False)
    core.sanic.exception_handler.register_exception_handler(server)
    server.register_listener(start, 'before_server_start')
    server.register_listener(do_start, 'after_server_start')
    server.register_listener(shutdown, 'before_server_stop')
    server.register_listener(do_shutdown, 'after_server_stop')
    server.register_middleware(qstd_core.sanic.server.utils.add_trace_id, 'request', priority=3)
    server.blueprint(router)
    return server


def start_server():
    server_config = config.server.http
    server = AppLoader(factory=create_http_server)
    app = server.load()
    app.prepare(
        host=server_config.host,
        port=server_config.port,
        workers=server_config.workers,
        access_log=True
    )
    app.shared_ctx.config = config_manager.get_multiprocessing_config_dict()
    return Sanic.serve(primary=app, app_loader=server)
