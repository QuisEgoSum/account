from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy_tx_context import SQLAlchemyTransactionContext

from src.core.config import config

connect_args = dict(
    max_cached_statement_lifetime=0,
    statement_cache_size=5000,
    server_settings={
        'application_name': config.project.name
    }
)


engine = create_async_engine(
    config.database.postgres.uri,
    connect_args=connect_args,
    pool_size=config.database.postgres.pool_size,
    max_overflow=0
)

db = SQLAlchemyTransactionContext(engine)


class Base(DeclarativeBase):
    __abstract__ = True
