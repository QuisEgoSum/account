import functools

from src.core.config import config


def logger_mode_traceback(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        try:
            record = args[1]
            if record.exc_text:
                print(record.exc_text)
        except:
            pass
        return result

    if config.logger.mode == 'traceback':
        return wrapper
    return func
