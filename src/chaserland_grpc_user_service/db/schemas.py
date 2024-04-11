from enum import Enum

from pydantic import BaseModel


class Scope(str, Enum):
    DEFAULT = None
    ADMIN = "admin"
    BLOG = "blog"
    BLOG_READ = "blog:r"
    BLOG_WRITE = "blog:w"


class OAuthBase(BaseModel):
    oauth_name: str
    oauth_id: str
    oauth_token_type: str
    oauth_access_token: str
    oauth_refresh_token: str | None
    oauth_issue_at: int
    oauth_expires_at: int | None
    oauth_scope: str | None


class OAuthCreate(OAuthBase):
    pass
