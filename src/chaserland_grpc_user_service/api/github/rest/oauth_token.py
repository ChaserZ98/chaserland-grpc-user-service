import base64
import urllib.parse

import aiohttp

from ..base_url import API_BASE_URL, OAUTH_BASE_URL
from ..exceptions import GithubApiException
from ..schemas import GithubOAuthToken
from ..version import VERSION as GITHUB_API_VERSION


def githubApiOAuthTokenExchangeEndpoint(
    code: str,
    client_id: str,
    client_secret: str,
    redirect_uri: str = "",
) -> str:
    base_url = OAUTH_BASE_URL
    path = "/login/oauth/access_token"
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
    }
    query = urllib.parse.urlencode(params)
    return f"{base_url}{path}?{query}"


def githubApiOAuthTokenEndpoint(
    client_id: str,
) -> str:
    base_url = API_BASE_URL
    path = f"/applications/{client_id}/token"
    return f"{base_url}{path}"


async def getOAuthToken(
    session: aiohttp.ClientSession,
    code: str,
    client_id: str,
    client_secret: str,
    redirect_uri: str = "",
) -> GithubOAuthToken:
    url = githubApiOAuthTokenExchangeEndpoint(
        code, client_id, client_secret, redirect_uri
    )
    headers = {"Accept": "application/json"}
    async with session.post(url, headers=headers) as response:
        if not response.ok:
            raise GithubApiException(**(await response.json()))

        body = await response.json()
        if "access_token" not in body:
            raise GithubApiException(
                message=body["error_description"],
                documentation_url=body["error_uri"],
            )

        return GithubOAuthToken(**(body))


async def checkOAuthToken(
    session: aiohttp.ClientSession,
    access_token: str,
    client_id: str,
    client_secret: str,
) -> bool:
    url = githubApiOAuthTokenEndpoint(client_id)
    basic_auth = f"{client_id}:{client_secret}"
    basic_auth = base64.b64encode(basic_auth.encode("utf-8")).decode("utf-8")
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Basic {basic_auth}",
        "X-GitHub-Api-Version": GITHUB_API_VERSION,
    }
    body = {"access_token": access_token}
    async with session.post(url, headers=headers, json=body) as response:
        if response.ok:
            return True
        raise GithubApiException(**(await response.json()))
