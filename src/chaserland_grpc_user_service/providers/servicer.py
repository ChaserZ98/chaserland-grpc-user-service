from chaserland_common.grpc import AbstractProvider
from chaserland_common.grpc.aio import Server as AIOgRPCServer
from chaserland_grpc_proto.protos.user import user_pb2_grpc as user_service

from ..servicer.user import UserServicer
from .oauth import GithubOAuthProvider


class ServicerProvider(AbstractProvider):
    @staticmethod
    def register(server: AIOgRPCServer) -> None:
        oauth_providers = [
            GithubOAuthProvider(),
        ]
        servicer = UserServicer(server_context_ref=server.context_ref)
        servicer.add_oauth_providers(oauth_providers)
        server.add_servicer(
            user_service.add_UserServicer_to_server,
            servicer,
        )
