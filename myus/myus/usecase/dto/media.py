from dataclasses import dataclass
from datetime import date, datetime
from myus.domain.channel.data import ChannelData
from myus.domain.hashtag.data import HashtagData
from myus.domain.media.audio.data import AudioData
from myus.domain.media.blog.data import BlogData
from myus.domain.media.chat.data import ChatData
from myus.domain.media.comic.data import ComicData
from myus.domain.media.hires.data import HiresData
from myus.domain.media.picture.data import PictureData
from myus.domain.media.video.data import VideoData
from myus.domain.payment.product.data import ProductData
from .comment import CommentDTO
from .message import MessageDTO
from .series import MediaSeriesDTO
from .user import MediaUserDTO


@dataclass(frozen=True, slots=True)
class HomeDTO:
    videos: list[VideoData]
    audios: list[AudioData]
    blogs: list[BlogData]
    comics: list[ComicData]
    pictures: list[PictureData]
    chats: list[ChatData]


@dataclass(frozen=True, slots=True)
class MediaCreateDTO:
    ulid: str


@dataclass(frozen=True, slots=True)
class MediaDetailDTO:
    id: int
    ulid: str
    title: str
    content: str
    read: int
    like: int
    publish: bool
    created: datetime
    updated: datetime
    channel: ChannelData
    mediaUser: MediaUserDTO
    hashtags: list[HashtagData]
    series: MediaSeriesDTO


@dataclass(frozen=True, slots=True)
class VideoDetailDTO(MediaDetailDTO):
    image: str
    video: str
    convert: str
    comments: list[CommentDTO]


@dataclass(frozen=True, slots=True)
class AudioDetailDTO(MediaDetailDTO):
    lyric: str
    image: str
    audio: str
    gain: float
    is_purchased: bool
    comments: list[CommentDTO]
    hires: HiresData | None
    product: ProductData | None


@dataclass(frozen=True, slots=True)
class BlogDetailDTO(MediaDetailDTO):
    richtext: str
    paid_text: str
    is_purchased: bool
    is_promotion: bool
    image: str
    comments: list[CommentDTO]
    product: ProductData | None


@dataclass(frozen=True, slots=True)
class ComicDetailDTO(MediaDetailDTO):
    image: str
    page_count: int
    is_purchased: bool
    pages: list[str]
    comments: list[CommentDTO]
    product: ProductData | None


@dataclass(frozen=True, slots=True)
class PictureDetailDTO(MediaDetailDTO):
    image: str
    comments: list[CommentDTO]


@dataclass(frozen=True, slots=True)
class ChatDetailDTO(MediaDetailDTO):
    thread: int
    joined: int
    period: date
    messages: list[MessageDTO]


@dataclass(frozen=True, slots=True)
class VideoCreateDTO:
    channel_ulid: str
    category_ulid: str
    publish: bool
    publish_at: datetime
    title: str
    content: str


@dataclass(frozen=True, slots=True)
class AudioCreateDTO:
    channel_ulid: str
    category_ulid: str
    publish: bool
    publish_at: datetime
    title: str
    content: str
    lyric: str


@dataclass(frozen=True, slots=True)
class BlogCreateDTO:
    channel_ulid: str
    category_ulid: str
    publish: bool
    publish_at: datetime
    title: str
    content: str
    richtext: str
    paid_text: str
    price: int
    is_promotion: bool


@dataclass(frozen=True, slots=True)
class ComicCreateDTO:
    channel_ulid: str
    category_ulid: str
    publish: bool
    publish_at: datetime
    title: str
    content: str


@dataclass(frozen=True, slots=True)
class PictureCreateDTO:
    channel_ulid: str
    category_ulid: str
    publish: bool
    publish_at: datetime
    title: str
    content: str


@dataclass(frozen=True, slots=True)
class ChatCreateDTO:
    channel_ulid: str
    category_ulid: str
    publish: bool
    publish_at: datetime
    title: str
    content: str
    period: date


@dataclass(frozen=True, slots=True)
class VideoUpdateDTO:
    category_ulid: str
    title: str
    content: str
    publish: bool
    publish_at: datetime


@dataclass(frozen=True, slots=True)
class AudioUpdateDTO:
    category_ulid: str
    title: str
    content: str
    lyric: str
    publish: bool
    publish_at: datetime


@dataclass(frozen=True, slots=True)
class BlogUpdateDTO:
    category_ulid: str
    title: str
    content: str
    richtext: str
    paid_text: str
    price: int
    is_promotion: bool
    publish: bool
    publish_at: datetime


@dataclass(frozen=True, slots=True)
class ComicUpdateDTO:
    category_ulid: str
    title: str
    content: str
    price: int
    free_pages: int
    publish: bool
    publish_at: datetime
    pages: list[str]


@dataclass(frozen=True, slots=True)
class PictureUpdateDTO:
    category_ulid: str
    title: str
    content: str
    publish: bool
    publish_at: datetime


@dataclass(frozen=True, slots=True)
class ChatUpdateDTO:
    category_ulid: str
    title: str
    content: str
    period: date
    publish: bool
    publish_at: datetime
