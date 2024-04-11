from datetime import datetime, timezone

import grpc
import grpc_interceptor.exceptions as grpc_exceptions
from chaserland_grpc_proto.protos.user import user_pb2 as user_message
from chaserland_grpc_proto.protos.user import user_pb2_grpc as user_service

from ..config.jwt import jwt_settings
from ..db import crud, schemas
from ..providers.oauth import GithubOAuthProvider
from ..utils.jwt import JWT, JWTHeader, JWTPayload
from ..utils.provider import OAuthProvider
from ..utils.servicer import AIOgRPCServicer


class UserServicer(user_service.UserServicer, AIOgRPCServicer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def github_oauth_provider(self):
        if not hasattr(self, "_github_oauth_provider"):
            raise AttributeError("Github OAuth provider is not set")
        return self._github_oauth_provider

    @github_oauth_provider.setter
    def github_oauth_provider(self, provider: GithubOAuthProvider):
        if hasattr(self, "_github_oauth_provider"):
            raise AttributeError("Github OAuth provider is already set")
        if not isinstance(provider, GithubOAuthProvider):
            raise TypeError(
                f"Expected GithubOAuthProvider instance, got {type(provider)}"
            )
        self._github_oauth_provider = provider

    def add_oauth_providers(self, providers: list[OAuthProvider]):
        for provider in providers:
            if isinstance(provider, GithubOAuthProvider):
                self.github_oauth_provider = provider
            else:
                raise TypeError(f"Unsupported OAuth provider: {type(provider)}")

    async def oauth_login(
        self, request: user_message.OAuthLoginRequest, context: grpc.ServicerContext
    ) -> user_message.OAuthLoginResponse:
        provider, code = request.provider, request.code
        if provider == user_message.OAUTH_PROVIDER_UNSPECIFIED:
            raise grpc_exceptions.InvalidArgument("OAuth provider is not specified")
        if provider == user_message.OAUTH_PROVIDER_GITHUB:
            oauth_token = await self.github_oauth_provider.get_token(
                code, self.server_context.http_session
            )
            oauth_info = await self.github_oauth_provider.get_user_info(
                oauth_token.access_token, self.server_context.http_session
            )
            oauth_id = f"github-{oauth_info.id}"
            oauth_name = "github"
            name = oauth_info.name if oauth_info.name else oauth_info.login
            email = oauth_info.email
            avatar = oauth_info.avatar_url
        async with self.server_context.db_session() as db:
            db_oauth_user = await crud.get_oauth_user_by_oauth_id(oauth_id, db)
            db_user = None
            if db_oauth_user is None:
                oauth_user = schemas.OAuthCreate(
                    oauth_name=oauth_name,
                    oauth_id=oauth_id,
                    oauth_token_type=oauth_token.token_type,
                    oauth_access_token=oauth_token.access_token,
                    oauth_refresh_token=None,
                    oauth_issue_at=int(datetime.now(timezone.utc).timestamp()),
                    oauth_expires_at=None,
                    oauth_scope=oauth_token.scope if oauth_token.scope else None,
                )
                db_user = await crud.create_user_with_oauth(oauth_user, db)
            else:
                patch = schemas.OAuthUpdate(
                    oauth_token_type=oauth_token.token_type,
                    oauth_access_token=oauth_token.access_token,
                    oauth_refresh_token=None,
                    oauth_issue_at=int(datetime.now(timezone.utc).timestamp()),
                    oauth_expires_at=None,
                    oauth_scope=oauth_token.scope if oauth_token.scope else None,
                )
                db_oauth_user = await crud.update_oauth_user(db_oauth_user, db, patch)
                db_user = db_oauth_user.user

            jwt_header = JWTHeader(alg=jwt_settings.ALGORITHM)
            jwt_payload = JWTPayload(
                id=db_user.id,
                scopes=db_user.scopes if db_user.scopes else [],
                name=name,
                email=email,
                avatar=avatar,
                iat=int(datetime.now(timezone.utc).timestamp()),
                exp=jwt_settings.EXPIRATION,
            )
            jwt = JWT(header=jwt_header, payload=jwt_payload)
            jwt_bearer = jwt.to_bearer(
                private_key=jwt_settings.PRIVATE_KEY.get_secret_value(),
                encoding="utf-8",
            )

        return user_message.OAuthLoginResponse(
            token_type=jwt_bearer.token_type,
            access_token=jwt_bearer.access_token,
        )
