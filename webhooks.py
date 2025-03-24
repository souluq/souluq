import argparse
import asyncio

import aiohttp

from app.config import env

parser = argparse.ArgumentParser()
parser.add_argument(
    "--url",
    type=str,
    help="url to send updates to",
    default="https://murat.a.pinggy.link/webhooks/telegram",
)
args = parser.parse_args()


async def setup_webhook():
    print("Setting up webhook")
    my_bot_token = env.TG_BOT_API_TOKEN
    webhook_token = env.TG_WEBHOOK_TOKEN
    url_to_send_updates_to = args.url
    url = f"https://api.telegram.org/bot{my_bot_token}/setWebhook?url={url_to_send_updates_to}&secret_token={webhook_token}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            r = await response.text()
            print(r)
            if response.status == 200:
                print("Webhook set up successfully to ", url_to_send_updates_to)
            else:
                print("Failed to set up webhook")


if __name__ == "__main__":
    asyncio.run(setup_webhook())
