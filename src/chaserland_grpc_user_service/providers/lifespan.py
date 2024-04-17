from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from chaserland_common.grpc import AbstractProvider, logger
from chaserland_common.grpc.aio import Server as AIOgRPCServer

from ..core.context import Context as AIOgRPCServerContext
from ..db.database import init_models


async def on_startup(app: AIOgRPCServer):
    logger.info(f"Starting server on {app.address}...")
    logger.info("Initializing db models...")
    await init_models()


async def on_shutdown(app: AIOgRPCServer):
    logger.info("Server stopped.")


@asynccontextmanager
async def lifespan(app: AIOgRPCServer) -> AsyncIterator[AIOgRPCServerContext]:
    await on_startup(app)
    async with AIOgRPCServerContext() as context:
        yield context
    await on_shutdown(app)


class LifespanProvider(AbstractProvider):
    @staticmethod
    def register(app: AIOgRPCServer):
        app.set_lifespan(lifespan)
