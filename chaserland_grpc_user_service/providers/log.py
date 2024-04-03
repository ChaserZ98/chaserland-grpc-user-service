import logging.config

from chaserland_grpc_user_service.config.logging import log_settings
from chaserland_grpc_user_service.utils.AIOgRPCServer import AIOgRPCServer
from chaserland_grpc_user_service.utils.provider import Provider


class LoggingProvider(Provider):
    @staticmethod
    def register(app: AIOgRPCServer):
        logging.config.dictConfig(log_settings.SERVER_LOG_CONFIG)
