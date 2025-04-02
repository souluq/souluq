from datetime import datetime

from fastapi import APIRouter, HTTPException, Request
from pydantic import ValidationError
from sqlalchemy import desc, select

from app.config import env
from app.db.engine import async_session_maker
from app.db.tables import Message
from app.llm import PROMPT
from app.llm.assistant import generate_response, get_audio
from app.telegram.messages import send_audio, send_message
from app.telegram.schemas import TelegramWebhookPayload

telegram_router = APIRouter(prefix="/telegram")


@telegram_router.post("")
async def telegram_webhook(request: Request):
    """
    Handle incoming webhook requests from Telegram.
    Setup telegram webhook to point to this endpoint:

    https://api.telegram.org/bot{my_bot_token}/setWebhook?url={url_to_send_updates_to}&secret_token={webhook_token}

    my_bot_token = env.TG_BOT_API_TOKEN

    webhook_token = env.TG_WEBHOOK_TOKEN
    """

    secret_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")

    if secret_token != env.TG_WEBHOOK_TOKEN:
        raise HTTPException(
            status_code=403,
            detail="Invalid secret token",
        )

    try:
        req_body = await request.json()
        body = TelegramWebhookPayload.model_validate(req_body)
        text = body.message.text
        date = datetime.now()

        if text.strip() == "/start":
            await send_message(body.message.chat.id, "Напишите любое сообщение")
            return {"success": True}

        if text.startswith("/speak"):
            msg_id = text.replace("/speak", "")
            audio = await get_audio(msg_id)
            if not audio:
                await send_message(body.message.chat.id, "Не удалось получить аудио")
                return {"success": True}

            await send_audio(body.message.chat.id, audio)

            return {"success": True}

        print(f"Received messages from {body.message.chat.username}: {text}")
        response_message, response_id = await generate_response(
            user_id=str(body.message.chat.id),
            message_id=f"{body.message.chat.id}-{body.message.message_id}",
            text=text,
        )
        resp_text = f"{response_message}\n\n/speak{response_id}"
        await send_message(body.message.chat.id, resp_text)

    except ValidationError:
        pass

    return {"success": True}
