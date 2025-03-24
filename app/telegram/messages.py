import aiohttp

from app.config import env


async def send_message(chat_id: int, text: str):
    url = f"https://api.telegram.org/bot{env.TG_BOT_API_TOKEN}/sendMessage"
    headers = {"Content-Type": "application/json"}
    data = {
        "chat_id": chat_id,
        "text": text,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            pass
