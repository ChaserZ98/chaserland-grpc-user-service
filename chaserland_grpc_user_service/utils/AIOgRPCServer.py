import asyncio
import logging

import grpc

from chaserland_grpc_user_service.config.app import app_settings

logger = logging.getLogger("grpc")


class AIOgRPCServer:
    def __init__(
        self,
        address: str = app_settings.server_address,
        graceful_shutdown_timeout: int = 5,
    ):
        self.server = grpc.aio.server()
        self.address = address
        self.graceful_shutdown_timeout = graceful_shutdown_timeout
        self.cleanup_coroutines = []
        self.loop = asyncio.get_event_loop()

        self.server.add_insecure_port(self.address)

    def add_servicer(self, register_func: callable, servicer):
        register_func(servicer, self.server)

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
            "Starting graceful shutdown... Allowing 5 seconds for ongoing calls to finish"
        )
        await self.server.stop(self.graceful_shutdown_timeout)
        logger.info("Server stopped.")

    async def start(self):
        logger.info("Starting server on %s", app_settings.server_address)
        await self.server.start()
        self.cleanup_coroutines.append(self.graceful_shutdown())
        await self.server.wait_for_termination()
