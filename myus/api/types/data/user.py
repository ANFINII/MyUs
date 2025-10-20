from dataclasses import dataclass
from ninja import Schema
from api.types.data.plan import PlanData


@dataclass(frozen=True, slots=True)
class UserData:
    avatar: str
    ulid: str
    nickname: str
    is_active: bool
    is_staff: bool


@dataclass(frozen=True, slots=True)
class UserInData:
    avatar: str | None
    email: str
    username: str
    nickname: str


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
    ulid: str
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
    is_confirmed: bool


@dataclass(frozen=True, slots=True)
class NotificationData:
    count: int
    datas: list[NotificationData]


@dataclass(frozen=True, slots=True)
class LikeOutData:
    is_like: bool
    like_count: int


class LikeMediaInData(Schema):
    id: int
    media_type: str


class LikeCommentInData(Schema):
    id: int
