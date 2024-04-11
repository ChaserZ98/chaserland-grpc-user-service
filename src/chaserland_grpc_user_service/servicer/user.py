import grpc
import grpc_interceptor.exceptions as grpc_exceptions
from chaserland_grpc_proto.protos.user import user_pb2 as user_message
from chaserland_grpc_proto.protos.user import user_pb2_grpc as user_service

from ..utils.servicer import AIOgRPCServicer


class UserServicer(user_service.UserServicer, AIOgRPCServicer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def oauth_login(
        self, request: user_message.OAuthLoginRequest, context: grpc.ServicerContext
    ) -> user_message.OAuthLoginResponse:
        raise grpc_exceptions.Unimplemented("OAuth login is not implemented yet")
