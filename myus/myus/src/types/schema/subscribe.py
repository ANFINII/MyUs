from pydantic import BaseModel


class SubscribeIn(BaseModel):
    channel_ulid: str
    is_subscribe: bool


class SubscribeOut(BaseModel):
    is_subscribe: bool
    count: int
