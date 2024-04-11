import asyncio
import logging
from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from typing import Self

import aiohttp
import grpc
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from ..config.app import app_settings
from ..db.database import async_session
from .ref import Ref

logger = logging.getLogger("grpc")


class Context(BaseModel, AbstractAsyncContextManager):
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


class AIOgRPCServer:
    def __init__(
        self,
        address: str = app_settings.server_address,
        graceful_shutdown_timeout: int = 5,
        lifespan: Callable[[Self], AbstractAsyncContextManager[Context]] = None,
        interceptors: list[grpc.ServerInterceptor] = None,
        loop: asyncio.AbstractEventLoop = None,
    ):
        self.interceptors = interceptors
        self.address = address
        self.graceful_shutdown_timeout = graceful_shutdown_timeout
        self.lifespan = lifespan
        self.context_ref: Ref[Context] = Ref()
        self.servicers = []

        self.loop = loop or asyncio.get_event_loop()

    def add_servicer(self, register_func: Callable, servicer):
        self.servicers.append((register_func, servicer))

    def set_lifespan(
        self, lifespan: Callable[[Self], AbstractAsyncContextManager[Context]]
    ):
        self.lifespan = lifespan

    def run(self):
        try:
            self.loop.run_until_complete(self.start())
        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt received.")
        finally:
            self.loop.run_until_complete(self.graceful_shutdown())
            self.loop.close()

    async def graceful_shutdown(self):
        logger.info(
            f"Starting graceful shutdown... Allowing {self.graceful_shutdown_timeout} seconds for ongoing calls to finish"
        )
        await self.server.stop(self.graceful_shutdown_timeout)

    async def start(self):
        self.server = grpc.aio.server(interceptors=self.interceptors)
        self.server.add_insecure_port(self.address)
        logger.info(f"Server created on {self.address}.")

        for register_func, servicer in self.servicers:
            register_func(servicer, self.server)
            logger.info(f"Servicer {servicer.__class__.__name__} added.")

        async with self.lifespan(self) as context:
            self.context_ref.current = context
            await self.server.start()
            await self.server.wait_for_termination()
            self.context_ref.current = None
