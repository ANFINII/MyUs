from datetime import datetime
from dataclasses import dataclass
from myus.api.types.data.comment import CommentData
from myus.api.types.dto.user import AuthorData


@dataclass(frozen=True, slots=True)
class HashtagData:
    jp_name: str


@dataclass(frozen=True, slots=True)
class VideoDetailData:
    id: int
    title: str
    content: str
    image: str
    video: str
    convert: str
    comments: list[CommentData]
    hashtags: list[HashtagData]
    like: int
    read: int
    comment_count: int
    publish: bool
    created: datetime
    updated: datetime
    author: AuthorData
