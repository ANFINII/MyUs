from dataclasses import dataclass
from api.src.domain.interface.notification.data import NotificationContentData as NotificationContentData


@dataclass(frozen=True, slots=True)
class NotificationUserDTO:
    avatar: str
    ulid: str
    nickname: str


@dataclass(frozen=True, slots=True)
class NotificationItemDTO:
    ulid: str
    user_from: NotificationUserDTO
    user_to: NotificationUserDTO | None
    type_no: int
    type_name: str
    content_object: NotificationContentData
    is_confirmed: bool


@dataclass(frozen=True, slots=True)
class NotificationDTO:
    count: int
    datas: list[NotificationItemDTO]
