from pydantic import BaseModel, Field


class From(BaseModel):
    id: int
    is_bot: bool | None = None
    first_name: str | None = None
    username: str | None = None
    language_code: str | None = None


class Chat(BaseModel):
    id: int
    first_name: str | None = None
    username: str | None = None
    type: str | None = None


class Message(BaseModel):
    message_id: int
    from_: From = Field(alias="from")
    chat: Chat
    date: int
    text: str


class TelegramWebhookPayload(BaseModel):
    update_id: int
    message: Message
