from datetime import datetime
from pydantic import BaseModel
from myus.utils.enum.media import EncodeStatus
from ..channel import ChannelOut
from ..comment import CommentOut
from ..message import MessageOut
from ..payment import ProductOut
from ..user import MediaUserOut


class MediaCreateOut(BaseModel):
    ulid: str


class MediaReadOut(BaseModel):
    read: int


class HiresUrlOut(BaseModel):
    url: str


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


class HiresOut(BaseModel):
    sample_rate: int
    bit_depth: int


class AudioOut(MediaOut):
    lyric: str
    image: str
    audio: str
    gain: float
    hires: HiresOut | None
    product: ProductOut | None


class BlogOut(MediaOut):
    richtext: str
    paid_text: str
    is_promotion: bool
    image: str
    product: ProductOut | None


class ComicOut(MediaOut):
    image: str
    pages: list[str]
    free_pages: int
    product: ProductOut | None


class PictureOut(MediaOut):
    image: str


class ChatOut(MediaOut):
    thread: int
    joined: int
    period: datetime


class VideoListOut(BaseModel):
    items: list[VideoOut]
    total: int


class AudioListOut(BaseModel):
    items: list[AudioOut]
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
    audios: list[AudioOut]
    blogs: list[BlogOut]
    comics: list[ComicOut]
    pictures: list[PictureOut]
    chats: list[ChatOut]


class VideoDetailOut(MediaDetailOut):
    image: str
    video: str
    convert: str
    comments: list[CommentOut]


class AudioDetailOut(MediaDetailOut):
    lyric: str
    image: str
    audio: str
    gain: float
    is_purchased: bool
    comments: list[CommentOut]
    hires: HiresOut | None
    product: ProductOut | None


class BlogDetailOut(MediaDetailOut):
    richtext: str
    paid_text: str
    is_purchased: bool
    is_promotion: bool
    image: str
    comments: list[CommentOut]
    product: ProductOut | None


class ComicDetailOut(MediaDetailOut):
    image: str
    page_count: int
    is_purchased: bool
    pages: list[str]
    comments: list[CommentOut]
    product: ProductOut | None


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


class AudioSeriesOut(BaseModel):
    ulid: str
    title: str
    items: list[AudioOut]


class AudioDetailsOut(BaseModel):
    detail: AudioDetailOut
    list: list[AudioOut]
    series: AudioSeriesOut


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
