from dataclasses import dataclass
from api.src.domain.interface.notification.data import NotificationContentData as NotificationContentData


@dataclass(frozen=True, slots=True)
class NotificationUserData:
    avatar: str
    ulid: str
    nickname: str


@dataclass(frozen=True, slots=True)
class NotificationItemData:
    ulid: str
    user_from: NotificationUserData
    user_to: NotificationUserData | None
    type_no: int
    type_name: str
    content_object: NotificationContentData
    is_confirmed: bool


@dataclass(frozen=True, slots=True)
class NotificationOutData:
    count: int
    datas: list[NotificationItemData]
