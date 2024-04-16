from sanic import Sanic, Request, response
from sanic.exceptions import RequestCancelled, SanicException

from qstd_core.exceptions import LocalizedException, BaseApplicationException
from qstd_core.validator.exceptions import SchemaValidationException
from src.core.logger import app_logger

logger = app_logger.getChild(__name__)


def register_exception_handler(app: Sanic):
    def get_request_data(request: Request):
        return dict(
            method=request.method,
            url=request.url,
            forwarded=request.headers.get("x-forwarded-for")
        )

    @app.exception(SchemaValidationException)
    def validation_exception_handler(_: Request, exception: SchemaValidationException):
        return response.json(exception.to_dict(), status=400)

    @app.exception(LocalizedException)
    def localization_exception_handler(request: Request, exception: LocalizedException):
        payload = exception.to_dict(request)
        logger.warn(
            'Localization exception',
            dict(
                exception=payload,
                status_code=exception.status_code,
                request=get_request_data(request)
            )
        )
        return response.json(payload, status=exception.status_code)

    @app.exception(SanicException)
    def exception_handler(request: Request, exception: SanicException):
        logger.warn(
            'Sanic exception',
            dict(
                exception=str(exception),
                exception_cls=str(type(exception)),
                status_code=exception.status_code,
                request=get_request_data(request)
            )
        )
        return response.json({'message': str(exception)}, status=exception.status_code)

    @app.exception(BaseApplicationException)
    def application_exception_handler(request: Request, exception: BaseApplicationException):
        payload = exception.to_dict()
        logger.warn(
            'Base exception',
            dict(
                exception=payload,
                status_code=exception.status_code,
                request=get_request_data(request)
            )
        )
        return response.json(payload, status=exception.status_code)

    # noinspection PyTypeChecker
    @app.exception(RequestCancelled)
    def cancelled_request_handler(request: Request, _: RequestCancelled):
        logger.warn(
            'Cancel request',
            dict(
                request=get_request_data(request)
            )
        )
        return response.empty()



