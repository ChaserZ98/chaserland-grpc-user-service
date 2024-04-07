import aiohttp
from api.github.rest.oauth_user import getOAuthUser

from src.api.github.rest.oauth_token import checkOAuthToken, getOAuthToken
from src.config.github import github_settings
from src.utils.provider import OAuthProvider


class GithubOAuthProvider(OAuthProvider):
    def __init__(
        self,
        client_id: str = github_settings.OAUTH_CLIENT_ID,
        client_secret: str = github_settings.OAUTH_CLIENT_SECRET.get_secret_value(),
    ):
        super().__init__(client_id, client_secret)

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

    async def get_user_info(self, access_token: str, session: aiohttp.ClientSession):
        return await getOAuthUser(session, access_token)

    async def check_token(self, access_token: str, session: aiohttp.ClientSession):
        return await checkOAuthToken(
            session, access_token, self.client_id, self.client_secret
        )
