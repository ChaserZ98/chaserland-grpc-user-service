from chaserland_grpc_user_service.providers.log import LoggingProvider
from chaserland_grpc_user_service.providers.servicer import ServicerProvider
from chaserland_grpc_user_service.utils.AIOgRPCServer import AIOgRPCServer, logger
from chaserland_grpc_user_service.utils.provider import Provider


def create_server() -> AIOgRPCServer:
    server = AIOgRPCServer()
    register(server, LoggingProvider)
    register(server, ServicerProvider)
    return server


def register(server: AIOgRPCServer, provider: Provider) -> None:
    provider.register(server)
    logger.info(provider.__name__ + " registered.")
