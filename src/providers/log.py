import logging.config

from src.config.logging import log_settings
from src.utils.AIOgRPCServer import AIOgRPCServer
from src.utils.provider import Provider


class LoggingProvider(Provider):
    @staticmethod
    def register(app: AIOgRPCServer):
        logging.config.dictConfig(log_settings.SERVER_LOG_CONFIG)
