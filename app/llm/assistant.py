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
    date: str,
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

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
            ]
            + [{"role": msg.role, "content": msg.content} for msg in messages],
        )
        response_text = response.choices[0].message.content

        response_date = datetime.now()
        ai_message = Message(
            id=response.id,
            user_id=user_id,
            content=response_text,
            response_id=response.id,
            role="assistant",
            date=response_date,
        )
        await create_message(session, ai_message)

    return response_text
