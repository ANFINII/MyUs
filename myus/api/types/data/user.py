from dataclasses import dataclass
from typing import Any
from api.types.data.plan import PlanData


@dataclass(frozen=True, slots=True)
class UserData:
    avatar: str
    email: str
    nickname: str
    is_active: bool
    is_staff: bool


@dataclass(frozen=True, slots=True)
class UserPlanData:
    plan: PlanData
    customer_id: str
    subscription: str
    is_paid: int
    start_date: int
    end_date: int


@dataclass(frozen=True, slots=True)
class AuthorData:
    avatar: str
    nickname: str
    follower_count: int


@dataclass(frozen=True, slots=True)
class MediaUserData:
    is_like: bool
    is_follow: bool


@dataclass(frozen=True, slots=True)
class NotificationUserData:
    avatar: int
    nickname: str


@dataclass(frozen=True, slots=True)
class NotificationData:
    id: int
    user_from: NotificationUserData
    user_to: NotificationUserData
    type_no: int
    type_name: str
    # content_object: Any
    is_confirmed: bool


@dataclass(frozen=True, slots=True)
class NotificationData:
    count: int
    datas: list[NotificationData]
