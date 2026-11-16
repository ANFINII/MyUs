from dataclasses import dataclass
from datetime import datetime
from myus.utils.enum.media import EncodeStatus
from ...channel.data import ChannelData
from ...hashtag.data import HashtagData


@dataclass(frozen=True, slots=True)
class VideoData:
    id: int
    ulid: str
    title: str
    content: str
    image: str
    video: str
    convert: str
    encode_status: EncodeStatus
    read: int
    like: int
    publish: bool
    publish_at: datetime
    created: datetime
    updated: datetime
    category_ulid: str
    channel: ChannelData
    hashtags: list[HashtagData]
