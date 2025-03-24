from datetime import datetime

from sqlalchemy import asc, select

from app.db.actions import create_message, create_user
from app.db.engine import async_session_maker
from app.db.tables import Message, User

from . import client, prompt


async def generate_response(
    user_id: str,
    message_id: str,
    text: str,
    date: datetime = datetime.now(),
):
    async with async_session_maker() as session:
        user = await session.execute(select(User).where(User.id == user_id))
        user = user.scalars().first()

        if user is None:
            user = User(id=user_id)
            await create_user(session, user)

        user_message = Message(
            id=message_id, user_id=user_id, content=text, role="user", date=date
        )
        await create_message(session, user_message)

        messages = await session.execute(
            select(Message)
            .where(
                Message.user_id == user_id,
            )
            .order_by(asc(Message.date))
        )
        messages = messages.scalars().all()

        response = client.responses.create(
            model="gpt-4o",
            input=[
                {"role": "system", "content": prompt},
            ]
            + [{"role": msg.role, "content": msg.content} for msg in messages],
        )

        ai_message = Message(
            id=response.id,
            user_id=user_id,
            content=response.output_text,
            response_id=response.id,
            role="assistant",
        )
        await create_message(session, ai_message)

    return response.output_text
