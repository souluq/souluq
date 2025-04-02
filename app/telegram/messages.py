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


async def send_audio(chat_id: int, audio: bytes):
    url = f"https://api.telegram.org/bot{env.TG_BOT_API_TOKEN}/sendAudio"

    # Create form data with the audio file
    form_data = aiohttp.FormData()
    form_data.add_field("chat_id", str(chat_id))
    form_data.add_field("audio", audio, filename="audio.mp3")

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=form_data) as response:
            pass
