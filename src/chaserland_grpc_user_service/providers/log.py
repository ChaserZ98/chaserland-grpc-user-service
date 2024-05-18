import logging.config
import os

from chaserland_common.grpc import AbstractProvider
from chaserland_common.grpc.aio import Server as AIOgRPCServer

from ..config.logging import log_settings


class LoggingProvider(AbstractProvider):
    @staticmethod
    def register(app: AIOgRPCServer):
        os.makedirs(log_settings.LOG_PATH, exist_ok=True)
        logging.config.dictConfig(log_settings.SERVER_LOG_CONFIG)
