import os

import yaml
from pydantic import BaseModel, Field

from qstd_config import ConfigManager, BaseConfig


root_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../../'))

with open(os.path.join(root_dir, 'project.yaml')) as stream:
    project_metadata = yaml.safe_load(stream)


class Config(BaseConfig):
    class Logger(BaseModel):
        level: str
        mode: str

    class Database(BaseModel):
        class Postgres(BaseModel, frozen=True):
            username: str
            password: str
            db: str
            host: str
            port: int
            uri: str
            pool_size: int

            def __init__(self, username: str, password: str, db: str, host: str, port: str, pool_size: int):
                super().__init__(
                    username=username,
                    password=password,
                    db=db,
                    host=host,
                    port=port,
                    pool_size=pool_size,
                    uri=f'postgresql+asyncpg://{username}:{password}@{host}:{port}/{db}',
                )
        postgres: Postgres

    class Server(BaseModel, frozen=True):
        class HttpServer(BaseModel, frozen=True):
            host: str = Field(min_length=1)
            port: int = Field(ge=1, le=65353)
            workers: int = Field(ge=1, le=124)

        class Address(BaseModel, frozen=True):
            docs: str

        http: HttpServer
        address: Address

    logger: Logger
    database: Database
    server: Server
    root_dir: str = root_dir


manager = ConfigManager(
    Config,
    project_metadata,
    config_paths=['./config/default.yaml'],
    root_config_dir=root_dir,
    multiprocessing_mode=True
)

config = manager.load_config()
