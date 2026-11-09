from typing import Annotated
from pydantic import BaseModel, Field


class ChannelIn(BaseModel):
    name: Annotated[str, Field(max_length=100)]
    description: str


class ChannelOut(BaseModel):
    ulid: str
    owner_ulid: str
    avatar: str
    name: str
    is_default: bool
    description: str
    count: int


class ChannelCreateOut(BaseModel):
    ulid: str
