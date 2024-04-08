import asyncio
import logging
from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from typing import Self

import aiohttp
import grpc
from pydantic import BaseModel, ConfigDict, Field

from src.config.app import app_settings
from src.utils.ref import Ref

logger = logging.getLogger("grpc")


class Context(BaseModel, AbstractAsyncContextManager):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    http_session: aiohttp.ClientSession = Field(
        frozen=True, default_factory=aiohttp.ClientSession
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
    ):
        self.server = grpc.aio.server(interceptors=interceptors)
        self.address = address
        self.graceful_shutdown_timeout = graceful_shutdown_timeout
        self.cleanup_coroutines = []
        self.loop = asyncio.get_event_loop()
        self.lifespan = lifespan

        self.server.add_insecure_port(self.address)
        self.context_ref: Ref[Context] = Ref()

    def add_servicer(self, register_func: callable, servicer):
        register_func(servicer, self.server)

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
            self.loop.run_until_complete(asyncio.gather(*self.cleanup_coroutines))
            self.loop.close()

    async def graceful_shutdown(self):
        logger.info(
            f"Starting graceful shutdown... Allowing {self.graceful_shutdown_timeout} seconds for ongoing calls to finish"
        )
        await self.server.stop(self.graceful_shutdown_timeout)

    async def start(self):
        async with self.lifespan(self) as context:
            self.context_ref.current = context
            await self.server.start()
            self.cleanup_coroutines.append(self.graceful_shutdown())
            await self.server.wait_for_termination()
            self.context_ref.current = None
