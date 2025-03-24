from sqlalchemy.ext.asyncio import AsyncSession

from .tables import Message, User


async def create_user(session: AsyncSession, user: User):
    session.add(user)
    await session.commit()
    await session.refresh(user)


async def create_message(session: AsyncSession, message: Message):
    session.add(message)
    await session.commit()
    await session.refresh(message)
