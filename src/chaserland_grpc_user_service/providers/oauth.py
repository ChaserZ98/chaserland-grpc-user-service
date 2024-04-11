import aiohttp
from chaserland_grpc_proto.protos.user import user_pb2 as user_message

from ..api.github.rest.oauth_token import checkOAuthToken, getOAuthToken
from ..api.github.rest.oauth_user import getOAuthUser
from ..config.github import github_settings
from ..utils.exception_handlers import OAuthExceptionHandler
from ..utils.provider import OAuthProvider


class GithubOAuthProvider(OAuthProvider):
    def __init__(
        self,
        client_id: str = github_settings.OAUTH_CLIENT_ID,
        client_secret: str = github_settings.OAUTH_CLIENT_SECRET.get_secret_value(),
    ):
        super().__init__(client_id, client_secret)

    @OAuthExceptionHandler(user_message.OAUTH_PROVIDER_GITHUB)
    async def get_token(
        self, code: str, session: aiohttp.ClientSession, redirect_uri: str = ""
    ):
        return await getOAuthToken(
            session,
            code,
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=redirect_uri,
        )

    @OAuthExceptionHandler(user_message.OAUTH_PROVIDER_GITHUB)
    async def get_user_info(self, access_token: str, session: aiohttp.ClientSession):
        return await getOAuthUser(session, access_token)

    @OAuthExceptionHandler(user_message.OAUTH_PROVIDER_GITHUB)
    async def check_token(self, access_token: str, session: aiohttp.ClientSession):
        return await checkOAuthToken(
            session, access_token, self.client_id, self.client_secret
        )
