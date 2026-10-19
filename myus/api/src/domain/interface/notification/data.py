from dataclasses import dataclass
from api.utils.enum.media import MediaType


@dataclass(frozen=True, slots=True)
class NotificationContentData:
    id: int
    ulid: str
    title: str
    text: str
    read: int
    media_type: MediaType | None
    media_ulid: str
    thread_ulid: str


@dataclass(frozen=True, slots=True)
class NotificationData:
    id: int
    ulid: str
    user_from_id: int
    user_to_id: int
    type_no: int
    type_name: str
    object_id: int
    object_type: str
    content: NotificationContentData | None
