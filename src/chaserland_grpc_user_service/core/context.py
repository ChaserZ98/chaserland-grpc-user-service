from typing import Self

import aiohttp
from chaserland_common.grpc.aio import AbstractContext
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from ..db.database import async_session


class Context(BaseModel, AbstractContext):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    http_session: aiohttp.ClientSession = Field(
        frozen=True, default_factory=aiohttp.ClientSession
    )
    db_session: async_sessionmaker[AsyncSession] = Field(
        frozen=True, default_factory=async_session
    )

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.http_session.close()
