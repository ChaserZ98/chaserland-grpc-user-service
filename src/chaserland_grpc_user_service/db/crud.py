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


async def update_oauth_user(
    oauth_user: models.OAuth, db: AsyncSession, oauth_patch: schemas.OAuthUpdate
):
    async with db.begin():
        for key, value in oauth_patch.model_dump().items():
            setattr(oauth_user, key, value)
    await db.refresh(oauth_user)
    return oauth_user
