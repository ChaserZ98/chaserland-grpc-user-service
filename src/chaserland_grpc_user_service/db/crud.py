from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def get_oauth_user_by_oauth_id(
    oauth_id: str, db: AsyncSession
) -> models.OAuth | None:
    res = None
    async with db.begin():
        res = (
            await db.execute(
                select(models.OAuth).where(models.OAuth.oauth_id == oauth_id)
            )
        ).scalar_one_or_none()
    return res


async def create_user_with_oauth(
    oauth_user: schemas.OAuthCreate, db: AsyncSession
) -> models.User:
    async with db.begin():
        db_user = models.User()
        db.add(db_user)
        await db.flush()
        await db.refresh(db_user)

        db_oauth_user = models.OAuth(**oauth_user.model_dump(), user_id=db_user.id)
        db.add(db_oauth_user)
        await db.flush()
        await db.refresh(db_oauth_user)

    await db.refresh(db_user)
    return db_user
