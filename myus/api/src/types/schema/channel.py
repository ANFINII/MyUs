from pydantic import BaseModel


class ChannelOut(BaseModel):
    ulid: str
    name: str
    is_default: bool
