from datetime import datetime
from pydantic import BaseModel
from api.src.types.schema.comment import CommentOut
from api.src.types.schema.message import MessageOut
from api.src.types.schema.channel import ChannelOut
from api.src.types.schema.user import MediaUserOut


class MediaCreateOut(BaseModel):
    ulid: str


class MediaOut(BaseModel):
    ulid: str
    title: str
    content: str
    read: int
    like: int
    publish: bool
    created: datetime
    updated: datetime
    channel: ChannelOut


class HashtagOut(BaseModel):
    jp_name: str


class MediaDetailOut(BaseModel):
    ulid: str
    title: str
    content: str
    read: int
    like: int
    publish: bool
    created: datetime
    updated: datetime
    channel: ChannelOut
    mediaUser: MediaUserOut
    hashtags: list[HashtagOut]


class VideoOut(MediaOut):
    image: str
    video: str
    convert: str


class MusicOut(MediaOut):
    lyric: str
    music: str
    download: bool


class ComicOut(MediaOut):
    image: str


class PictureOut(MediaOut):
    image: str


class BlogOut(MediaOut):
    image: str


class ChatOut(MediaOut):
    thread: int
    joined: int
    period: datetime


class HomeOut(BaseModel):
    videos: list[VideoOut]
    musics: list[MusicOut]
    comics: list[ComicOut]
    pictures: list[PictureOut]
    blogs: list[BlogOut]
    chats: list[ChatOut]


class VideoDetailOut(MediaDetailOut):
    image: str
    video: str
    convert: str
    comments: list[CommentOut]


class MusicDetailOut(MediaDetailOut):
    lyric: str
    music: str
    download: bool
    comments: list[CommentOut]


class ComicDetailOut(MediaDetailOut):
    image: str
    pages: list[str]
    comments: list[CommentOut]


class PictureDetailOut(MediaDetailOut):
    image: str
    comments: list[CommentOut]


class BlogDetailOut(MediaDetailOut):
    richtext: str
    image: str
    comments: list[CommentOut]


class ChatDetailOut(MediaDetailOut):
    thread: int
    joined: int
    period: datetime
    messages: list[MessageOut]


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
