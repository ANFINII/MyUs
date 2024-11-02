from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class UserOut:
    avatar: str
    email: str
    nickname: str
    is_active: bool
    is_staff: bool


@dataclass(frozen=True)
class Author:
    avatar: str
    nickname: str
    follower_count: int


@dataclass(frozen=True)
class MediaUser:
    avatar: str
    nickname: str
    is_like: bool
    is_follow: bool


@dataclass(frozen=True)
class NotificationUser:
    avatar: int
    nickname: str


@dataclass(frozen=True)
class NotificationData:
    id: int
    user_from: NotificationUser
    user_to: NotificationUser
    type_no: int
    type_name: str
    content_object: Any
    is_confirmed: bool


@dataclass(frozen=True)
class NotificationOut:
    count: int
    datas: list[NotificationData]
