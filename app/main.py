from fastapi import FastAPI

from app.db.engine import create_db_and_tables
from app.routers import webhooks


async def on_startup():
    await create_db_and_tables()


app = FastAPI()
app.add_event_handler("startup", on_startup)
app.include_router(webhooks.router)
