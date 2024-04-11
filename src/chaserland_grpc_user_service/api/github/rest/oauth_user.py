import aiohttp

from ..base_url import API_BASE_URL
from ..exceptions import GithubApiException
from ..schemas import GithubOAuthUser
from ..version import VERSION as GITHUB_API_VERSION


def githubApiOAuthUserEndpoint() -> str:
    base_url = API_BASE_URL
    path = "/user"
    return f"{base_url}{path}"


async def getOAuthUser(
    session: aiohttp.ClientSession,
    oauth_token: str,
) -> GithubOAuthUser:
    url = githubApiOAuthUserEndpoint()
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {oauth_token}",
        "X-GitHub-Api-Version": GITHUB_API_VERSION,
    }
    async with session.get(url, headers=headers) as response:
        if not response.ok:
            raise GithubApiException(**(await response.json()))
        return GithubOAuthUser(**(await response.json()))
