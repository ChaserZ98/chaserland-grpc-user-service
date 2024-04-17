from abc import ABC, abstractmethod
from typing import Any


class OAuthProvider(ABC):
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    @abstractmethod
    async def get_token(self, code: str, session: Any):
        raise NotImplementedError

    @abstractmethod
    async def check_token(self, access_token: str, session: Any):
        raise NotImplementedError
