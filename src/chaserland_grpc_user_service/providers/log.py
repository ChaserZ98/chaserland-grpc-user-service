import logging.config

from ..config.logging import log_settings
from ..utils.AIOgRPCServer import AIOgRPCServer
from ..utils.provider import Provider


class LoggingProvider(Provider):
    @staticmethod
    def register(app: AIOgRPCServer):
        logging.config.dictConfig(log_settings.SERVER_LOG_CONFIG)
