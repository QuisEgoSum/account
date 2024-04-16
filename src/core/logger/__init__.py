import logging

from qstd_logger_json_formatter import JsonFormatter, configure

from src.core.config import config

from .decorators import logger_mode_traceback


class FormatterWrapper(JsonFormatter):
    @logger_mode_traceback
    def format(self, record):
        return super().format(record)


FormatterWrapper\
    .set_parse_payload_root_logger('app') \
    .set_formatter(
        'sanic.access',
        lambda record: dict(
            level=record.levelname,
            message=record.message,
            host=record.host,
            request=record.request,
            status=record.status,
            byte=record.byte,
            label=record.name,
            pname=record.processName,
            pid=record.process,
            timestamp=record.asctime
        )
    )

configure(FormatterWrapper)

app_logger = logging.getLogger('app')

LOGGING_CONFIG = dict(
    version=1,
    disable_existing_loggers=False,
    loggers={
        "sanic.root": {
            "level": "INFO"
        },
        "sanic.error": {
            "level": "INFO",
            "propagate": True,
            "qualname": "sanic.error"
        },
        "sanic.access": {
            "level": "INFO",
            "propagate": True,
            "qualname": "sanic.access"
        },
        "app": {
            "level": config.logger.level,
            "propagate": True,
            "qualname": "app"
        }
    }
)
