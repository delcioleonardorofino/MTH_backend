from sqlalchemy import select
from ...models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

type(User.id)

async def fetch_all_users(db:AsyncSession):

    result = await db.execute(
        select(User)
        )
    users = result.scalars().all()

    return users

async def fetch_user_by_id(user_id: str, db: AsyncSession):

    result = await db.execute(
        select(User).where(User.id==UUID(user_id))
        )
    user = result.scalar_one_or_none()

    return user