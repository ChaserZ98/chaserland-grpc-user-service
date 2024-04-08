from pydantic import BaseModel


class GithubOAuthToken(BaseModel):
    token_type: str
    scope: str
    access_token: str


class GithubOAuthUser(BaseModel):
    login: str
    id: int
    node_id: str
    avatar_url: str
    gravatar_id: str
    url: str
    html_url: str
    followers_url: str
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: str
    organizations_url: str
    repos_url: str
    events_url: str
    received_events_url: str
    type: str
    site_admin: bool
    name: str
    company: str
    blog: str
    location: str
    email: str | None
    hireable: bool
    bio: str
    twitter_username: str | None
    public_repos: int
    public_gists: int
    followers: int
    following: int
    created_at: str
    updated_at: str
