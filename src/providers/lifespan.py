from contextlib import asynccontextmanager
from typing import AsyncIterator

from src.utils.AIOgRPCServer import AIOgRPCServer, logger
from src.utils.provider import Provider


async def on_startup(app: AIOgRPCServer):
    logger.info("Starting server on %s", app.address)


async def on_shutdown(app: AIOgRPCServer):
    logger.info("Server stopped.")


@asynccontextmanager
async def lifespan(app: AIOgRPCServer) -> AsyncIterator[dict]:
    await on_startup(app)
    yield {}
    await on_shutdown(app)


class LifespanProvider(Provider):
    @staticmethod
    def register(app: AIOgRPCServer):
        app.set_lifespan(lifespan)
