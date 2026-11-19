from datetime import datetime
from pydantic import BaseModel
from myus.utils.enum.media import EncodeStatus
from ..channel import ChannelOut
from ..comment import CommentOut
from ..message import MessageOut
from ..payment import MoneyOut
from ..user import MediaUserOut


class MediaCreateOut(BaseModel):
    ulid: str


class MediaReadOut(BaseModel):
    read: int


class MediaOut(BaseModel):
    ulid: str
    title: str
    content: str
    read: int
    like: int
    publish: bool
    publish_at: datetime
    created: datetime
    updated: datetime
    category_ulid: str
    channel: ChannelOut


class HashtagOut(BaseModel):
    ulid: str
    name: str


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
    encode_status: EncodeStatus


class MusicOut(MediaOut):
    lyric: str
    image: str
    music: str
    gain: float


class BlogOut(MediaOut):
    richtext: str
    price: MoneyOut
    is_promotion: bool
    image: str


class ManageBlogOut(BlogOut):
    paid_text: str


class ComicOut(MediaOut):
    image: str
    pages: list[str]


class PictureOut(MediaOut):
    image: str


class ChatOut(MediaOut):
    thread: int
    joined: int
    period: datetime


class VideoListOut(BaseModel):
    items: list[VideoOut]
    total: int


class MusicListOut(BaseModel):
    items: list[MusicOut]
    total: int


class BlogListOut(BaseModel):
    items: list[BlogOut]
    total: int


class ComicListOut(BaseModel):
    items: list[ComicOut]
    total: int


class PictureListOut(BaseModel):
    items: list[PictureOut]
    total: int


class ChatListOut(BaseModel):
    items: list[ChatOut]
    total: int


class HomeOut(BaseModel):
    videos: list[VideoOut]
    musics: list[MusicOut]
    blogs: list[BlogOut]
    comics: list[ComicOut]
    pictures: list[PictureOut]
    chats: list[ChatOut]


class VideoDetailOut(MediaDetailOut):
    image: str
    video: str
    convert: str
    comments: list[CommentOut]


class MusicDetailOut(MediaDetailOut):
    lyric: str
    image: str
    music: str
    gain: float
    comments: list[CommentOut]


class BlogDetailOut(MediaDetailOut):
    richtext: str
    paid_text: str
    price: MoneyOut
    is_purchased: bool
    is_promotion: bool
    image: str
    comments: list[CommentOut]


class ComicDetailOut(MediaDetailOut):
    image: str
    pages: list[str]
    comments: list[CommentOut]


class PictureDetailOut(MediaDetailOut):
    image: str
    comments: list[CommentOut]


class ChatDetailOut(MediaDetailOut):
    thread: int
    joined: int
    period: datetime
    messages: list[MessageOut]


class VideoSeriesOut(BaseModel):
    ulid: str
    title: str
    items: list[VideoOut]


class VideoDetailsOut(BaseModel):
    detail: VideoDetailOut
    list: list[VideoOut]
    series: VideoSeriesOut


class MusicSeriesOut(BaseModel):
    ulid: str
    title: str
    items: list[MusicOut]


class MusicDetailsOut(BaseModel):
    detail: MusicDetailOut
    list: list[MusicOut]
    series: MusicSeriesOut


class BlogSeriesOut(BaseModel):
    ulid: str
    title: str
    items: list[BlogOut]


class BlogDetailsOut(BaseModel):
    detail: BlogDetailOut
    list: list[BlogOut]
    series: BlogSeriesOut


class ComicSeriesOut(BaseModel):
    ulid: str
    title: str
    items: list[ComicOut]


class ComicDetailsOut(BaseModel):
    detail: ComicDetailOut
    list: list[ComicOut]
    series: ComicSeriesOut


class PictureSeriesOut(BaseModel):
    ulid: str
    title: str
    items: list[PictureOut]


class PictureDetailsOut(BaseModel):
    detail: PictureDetailOut
    list: list[PictureOut]
    series: PictureSeriesOut


class ChatSeriesOut(BaseModel):
    ulid: str
    title: str
    items: list[ChatOut]


class ChatDetailsOut(BaseModel):
    detail: ChatDetailOut
    list: list[ChatOut]
    series: ChatSeriesOut
