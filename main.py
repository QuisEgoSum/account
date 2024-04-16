import sys
import logging.config

from src.core.logger import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)


if __name__ == '__main__':
    SERVICE_NAME = sys.argv[1]
    if SERVICE_NAME == 'http':
        from src.apps.http.main import main
        main()
    else:
        raise NotImplementedError()
