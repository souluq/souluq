from datetime import datetime
from tempfile import NamedTemporaryFile

from openai import AsyncOpenAI
from sqlalchemy import asc, desc, select

from app.db.actions import create_message, create_user
from app.db.engine import async_session_maker
from app.db.tables import Message, User

from . import PROMPT

ai = AsyncOpenAI()


async def generate_response(
    user_id: str,
    message_id: str,
    text: str,
) -> tuple[str, str]:
    async with async_session_maker() as session:
        user = await session.execute(select(User).where(User.id == user_id))
        user = user.scalars().first()

        if user is None:
            user = User(id=user_id)
            await create_user(session, user)

        user_message = Message(
            id=message_id, user_id=user_id, content=text, role="user"
        )
        await create_message(session, user_message)

        messages = await session.execute(
            select(Message)
            .where(Message.user_id == user_id, Message.role == "assistant")
            .order_by(desc(Message.date))
            .limit(1)
        )
        last_response = messages.scalars().first()

        prompt = {
            "role": "developer",
            "content": [{"type": "input_text", "text": PROMPT}],
        }

        human_input = {
            "role": "user",
            "content": [{"type": "input_text", "text": text}],
        }

        ai_input = text if last_response else [prompt, human_input]

        response = await ai.responses.create(
            model="gpt-4o",
            input=ai_input,
            previous_response_id=last_response.id if last_response else None,
        )
        response_text = response.output_text

        ai_message = Message(
            id=response.id,
            user_id=user_id,
            content=response_text,
            response_id=response.id,
            role="assistant",
        )
        await create_message(session, ai_message)

    return response_text, response.id


async def get_audio(msg_id: str) -> bytes | None:
    async with async_session_maker() as session:
        message = await session.execute(select(Message).where(Message.id == msg_id))
        message = message.scalars().first()
        if not message:
            return None

        audio = await ai.audio.speech.create(
            input=message.content,
            model="gpt-4o-mini-tts",
            voice="sage",
            instructions="You are a female therapist. Speak in a clear, warm and calm tone while maintaining professionalism.",
        )

        return audio.content
