from dataclasses import dataclass
from typing import Self

import aiohttp
from chaserland_common.grpc.aio import AbstractContext
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from ..db.database import async_session


@dataclass(frozen=True)
class Context(AbstractContext):
    http_session: aiohttp.ClientSession = aiohttp.ClientSession()

    db_session: async_sessionmaker[AsyncSession] = async_session

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.http_session.close()
