from datetime import datetime
from pydantic import BaseModel
from api.src.types.schema.user import AuthorOut


class MessageCreateIn(BaseModel):
    chat_ulid: str
    text: str
    parent_ulid: str = ""


class MessageUpdateIn(BaseModel):
    chat_ulid: str
    text: str


class ChatMessageReplyOut(BaseModel):
    ulid: str
    parent_id: str
    text: str
    created: datetime
    updated: datetime
    author: AuthorOut


class ChatMessageOut(BaseModel):
    ulid: str
    text: str
    reply_count: int
    created: datetime
    updated: datetime
    author: AuthorOut
