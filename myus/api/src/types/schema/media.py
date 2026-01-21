from datetime import datetime
from pydantic import BaseModel
from api.src.types.schema.comment import CommentOut
from api.src.types.schema.message import ChatMessageOut
from api.src.types.schema.user import AuthorOut, MediaUserOut


# Inputs

class VideoIn(BaseModel):
    title: str
    content: str
    channel_ulid: str


class MusicIn(BaseModel):
    title: str
    content: str
    lyric: str
    download: bool
    channel_ulid: str


class ComicIn(BaseModel):
    title: str
    content: str
    channel_ulid: str


class PictureIn(BaseModel):
    title: str
    content: str
    channel_ulid: str


class BlogIn(BaseModel):
    title: str
    content: str
    richtext: str
    channel_ulid: str


class ChatIn(BaseModel):
    title: str
    content: str
    period: str
    channel_ulid: str


# Outputs

class HashtagOut(BaseModel):
    jp_name: str


class MediaCreateOut(BaseModel):
    ulid: str


class MediaOut(BaseModel):
    ulid: str
    title: str
    content: str
    read: int
    like_count: int
    publish: bool
    created: datetime
    updated: datetime
    author: AuthorOut


class MediaDetailOut(BaseModel):
    ulid: str
    title: str
    content: str
    read: int
    like_count: int
    publish: bool
    created: datetime
    updated: datetime
    author: AuthorOut
    mediaUser: MediaUserOut
    hashtags: list[HashtagOut]


class VideoOut(MediaOut):
    image: str
    video: str
    convert: str
    comment_count: int


class VideoDetailOut(MediaDetailOut):
    image: str
    video: str
    convert: str
    comments: list[CommentOut]


class MusicOut(MediaOut):
    lyric: str
    music: str
    download: bool
    comment_count: int


class MusicDetailOut(MediaDetailOut):
    lyric: str
    music: str
    download: bool
    comments: list[CommentOut]


class ComicOut(MediaOut):
    image: str
    comment_count: int


class ComicDetailOut(MediaDetailOut):
    image: str
    comments: list[CommentOut]


class PictureOut(MediaOut):
    image: str
    comment_count: int


class PictureDetailOut(MediaDetailOut):
    image: str
    comments: list[CommentOut]


class BlogOut(MediaOut):
    image: str
    comment_count: int


class BlogDetailOut(MediaDetailOut):
    richtext: str
    image: str
    comments: list[CommentOut]


class ChatOut(MediaOut):
    thread: int
    joined: int
    period: datetime


class ChatDetailOut(MediaDetailOut):
    thread: int
    joined: int
    period: datetime
    messages: list[ChatMessageOut]


class HomeOut(BaseModel):
    videos: list[VideoOut]
    musics: list[MusicOut]
    comics: list[ComicOut]
    pictures: list[PictureOut]
    blogs: list[BlogOut]
    chats: list[ChatOut]


class VideoDetailsOut(BaseModel):
    detail: VideoDetailOut
    list: list[VideoOut]


class MusicDetailsOut(BaseModel):
    detail: MusicDetailOut
    list: list[MusicOut]


class ComicDetailsOut(BaseModel):
    detail: ComicDetailOut
    list: list[ComicOut]


class PictureDetailsOut(BaseModel):
    detail: PictureDetailOut
    list: list[PictureOut]


class BlogDetailsOut(BaseModel):
    detail: BlogDetailOut
    list: list[BlogOut]


class ChatDetailsOut(BaseModel):
    detail: ChatDetailOut
    list: list[ChatOut]
