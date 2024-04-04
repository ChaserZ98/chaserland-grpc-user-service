from src.providers.lifespan import LifespanProvider
from src.providers.log import LoggingProvider
from src.providers.servicer import ServicerProvider
from src.utils.AIOgRPCServer import AIOgRPCServer, logger
from src.utils.interceptors import (
    AsyncAccessLoggerInterceptor,
    AsyncExceptionToStatusInterceptor,
)
from src.utils.provider import Provider


def create_server() -> AIOgRPCServer:
    interceptors = [AsyncAccessLoggerInterceptor(), AsyncExceptionToStatusInterceptor()]
    server = AIOgRPCServer(interceptors=interceptors)
    register(server, LoggingProvider)
    register(server, LifespanProvider)
    register(server, ServicerProvider)
    return server


def register(server: AIOgRPCServer, provider: Provider) -> None:
    provider.register(server)
    logger.info(provider.__name__ + " registered.")
