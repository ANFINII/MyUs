from pydantic import BaseModel


class ChannelOut(BaseModel):
    ulid: str
    avatar: str
    name: str
    is_default: bool
    description: str
