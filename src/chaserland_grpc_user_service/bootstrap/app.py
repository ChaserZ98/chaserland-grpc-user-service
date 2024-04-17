from chaserland_common.grpc import AbstractProvider, logger
from chaserland_common.grpc.aio import (
    AsyncAccessLoggerInterceptor,
    AsyncExceptionToStatusInterceptor,
)
from chaserland_common.grpc.aio import Server as AIOgRPCServer

from ..config.app import app_settings
from ..providers.lifespan import LifespanProvider
from ..providers.log import LoggingProvider
from ..providers.servicer import ServicerProvider


def create_server() -> AIOgRPCServer:
    interceptors = [AsyncAccessLoggerInterceptor(), AsyncExceptionToStatusInterceptor()]
    server = AIOgRPCServer(
        address=app_settings.server_address, interceptors=interceptors
    )
    register(server, LoggingProvider)
    register(server, LifespanProvider)
    register(server, ServicerProvider)
    return server


def register(server: AIOgRPCServer, provider: AbstractProvider) -> None:
    provider.register(server)
    logger.info(provider.__name__ + " registered.")
