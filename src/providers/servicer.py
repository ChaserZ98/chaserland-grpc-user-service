from chaserland_grpc_proto.protos.user import user_pb2_grpc as user_service

from src.servicer.user import UserServicer
from src.utils.AIOgRPCServer import AIOgRPCServer
from src.utils.provider import Provider


class ServicerProvider(Provider):
    @staticmethod
    def register(server: AIOgRPCServer) -> None:
        server.add_servicer(
            user_service.add_UserServicer_to_server,
            UserServicer(server_context_ref=server.context_ref),
        )
