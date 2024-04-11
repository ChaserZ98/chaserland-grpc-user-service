from ..providers.lifespan import LifespanProvider
from ..providers.log import LoggingProvider
from ..providers.servicer import ServicerProvider
from ..utils.AIOgRPCServer import AIOgRPCServer, logger
from ..utils.interceptors import (
    AsyncAccessLoggerInterceptor,
    AsyncExceptionToStatusInterceptor,
)
from ..utils.provider import Provider


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
