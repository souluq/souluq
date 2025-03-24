import asyncio
import uuid

from app.config import env
from app.llm.assistant import generate_response


async def main():
    user_id = "cli"

    while True:
        user_query = input(f"User: ")

        if user_query.lower() in ["q", "й", "quit"]:
            break

        message_id = str(uuid.uuid4())

        response = await generate_response(user_id, message_id, user_query)
        print(f"{env.AI_NAME}:", response)


if __name__ == "__main__":
    asyncio.run(main())
