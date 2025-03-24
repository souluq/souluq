from fastapi import APIRouter

from .telegram import telegram_router

router = APIRouter(prefix="/webhooks")
router.include_router(telegram_router)
