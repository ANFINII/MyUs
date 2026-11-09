from typing import Annotated
from pydantic import BaseModel, Field
from api.utils.enum.media import MediaType


class UserOut(BaseModel):
    avatar: str
    ulid: str
    nickname: str
    is_active: bool
    is_staff: bool


class AuthorOut(BaseModel):
    avatar: str
    ulid: str
    nickname: str
    follower_count: int


class MediaUserOut(BaseModel):
    is_like: bool
    is_subscribe: bool


class SearchTagIn(BaseModel):
    sequence: int
    name: Annotated[str, Field(max_length=30)]


class SearchTagOut(BaseModel):
    sequence: int
    name: str


class LikeOut(BaseModel):
    is_like: bool
    like_count: int


class LikeMediaIn(BaseModel):
    ulid: str
    media_type: MediaType


class LikeCommentIn(BaseModel):
    ulid: str
