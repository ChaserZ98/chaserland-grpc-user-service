from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from ..config.db import db_settings

engine = create_async_engine(
    db_settings.ASYNC_URL.get_secret_value(),
    pool_pre_ping=True,
    connect_args={
        "timeout": 10,
        "server_settings": {"search_path": db_settings.SCHEMA.get_secret_value()},
    },
)

async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


async def init_models():
    from .models import LocalAuth, OAuth, User

    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
