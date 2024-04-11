from collections.abc import Awaitable, Callable
from functools import wraps

import grpc_interceptor.exceptions as grpc_exceptions
from chaserland_grpc_proto.protos.user import user_pb2 as user_message

from ..api.github.exceptions import GithubApiException


class OAuthExceptionHandler:
    def __init__(self, oauth_provider: user_message.OAuthProvider) -> None:
        if oauth_provider == user_message.OAUTH_PROVIDER_UNSPECIFIED:
            raise ValueError("OAuth provider is not specified")
        if oauth_provider == user_message.OAUTH_PROVIDER_GITHUB:
            self.OAuthException = GithubApiException
            self.oauth_type = "Github"
            return
        raise ValueError(f"Unsupported OAuth provider: {oauth_provider}")

    def __call__[**P, T](
        self, func: Callable[P, Awaitable[T]]
    ) -> Callable[P, Awaitable[T]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            try:
                return await func(*args, **kwargs)
            except self.OAuthException as e:
                raise grpc_exceptions.Unauthenticated(
                    f"{self.oauth_type} API error: {e.message}"
                )
            except Exception as e:
                raise grpc_exceptions.Internal(
                    f"Failed to get {self.oauth_type} token: {e}"
                )

        return wrapper
