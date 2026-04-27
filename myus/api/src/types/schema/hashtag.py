from pydantic import BaseModel
from api.utils.enum.index import MediaType


class HashtagItemIn(BaseModel):
    ulid: str
    name: str


class MediaHashtagsUpdateIn(BaseModel):
    media_type: MediaType
    media_ulid: str
    hashtags: list[HashtagItemIn]


class HashtagOut(BaseModel):
    ulid: str
    name: str
