from chaserland_grpc_proto.protos.user import user_pb2_grpc as user_service

from chaserland_grpc_user_service.servicer.user import UserServicer
from chaserland_grpc_user_service.utils.AIOgRPCServer import AIOgRPCServer
from chaserland_grpc_user_service.utils.provider import Provider


class ServicerProvider(Provider):
    @staticmethod
    def register(server: AIOgRPCServer) -> None:
        server.add_servicer(user_service.add_UserServicer_to_server, UserServicer())
