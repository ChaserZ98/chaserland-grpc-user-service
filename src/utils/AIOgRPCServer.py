import asyncio
import logging
from typing import AsyncIterator, List

import grpc

from src.config.app import app_settings

logger = logging.getLogger("grpc")


class AIOgRPCServer:
    context: dict

    def __init__(
        self,
        address: str = app_settings.server_address,
        graceful_shutdown_timeout: int = 5,
        lifespan: callable = None,
        interceptors: List[grpc.ServerInterceptor] = None,
    ):
        self.server = grpc.aio.server(interceptors=interceptors)
        self.address = address
        self.graceful_shutdown_timeout = graceful_shutdown_timeout
        self.cleanup_coroutines = []
        self.loop = asyncio.get_event_loop()
        self.lifespan = lifespan

        self.server.add_insecure_port(self.address)

    def add_servicer(self, register_func: callable, servicer):
        register_func(servicer, self.server)

    def set_lifespan(self, lifespan: AsyncIterator[dict]):
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
            self.context = context
            await self.server.start()
            self.cleanup_coroutines.append(self.graceful_shutdown())
            await self.server.wait_for_termination()
            self.context = None
