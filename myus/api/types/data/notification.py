from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NotificationUserData:
    avatar: str
    nickname: str


@dataclass(frozen=True, slots=True)
class NotificationContentData:
    id: int


@dataclass(frozen=True, slots=True)
class NotificationItemData:
    id: int
    user_from: NotificationUserData
    user_to: NotificationUserData
    type_no: int
    type_name: str
    content_object: NotificationContentData
    is_confirmed: bool


@dataclass(frozen=True, slots=True)
class NotificationOutData:
    count: int
    datas: list[NotificationItemData]
