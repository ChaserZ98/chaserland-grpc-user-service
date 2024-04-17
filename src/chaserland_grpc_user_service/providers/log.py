import logging.config

from chaserland_common.grpc import AbstractProvider
from chaserland_common.grpc.aio import Server as AIOgRPCServer

from ..config.logging import log_settings


class LoggingProvider(AbstractProvider):
    @staticmethod
    def register(app: AIOgRPCServer):
        logging.config.dictConfig(log_settings.SERVER_LOG_CONFIG)
