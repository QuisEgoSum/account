from datetime import datetime

from gino import Gino
from sanic.log import logger as default_logger

from src.core.config import config


logger = default_logger.getChild('db')

db = Gino()


class DefaultModel(db.Model):
    id = db.Column(db.Integer(), primary_key=True)


class TimestampedModel(DefaultModel):
    created_at = db.Column(db.Integer(), nullable=False, default=lambda: int(datetime.now().timestamp()))
    updated_at = db.Column(db.Integer(), nullable=False, default=lambda: int(datetime.now().timestamp()))


async def connect():
    logger.info('DB connecting')
    await db.set_bind(config.database.uri)
    logger.info('DB connected')


async def disconnect():
    logger.info('DB disconnecting')
    await db.pop_bind().close()
    logger.info('DB disconnected')
