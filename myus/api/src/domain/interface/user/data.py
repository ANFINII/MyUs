from dataclasses import dataclass
from datetime import date
from ninja import UploadedFile
from api.src.types.data.plan import PlanData


@dataclass(frozen=True, slots=True)
class UserData:
    id: int
    ulid: str
    avatar: str | UploadedFile
    password: str
    email: str
    username: str
    nickname: str
    is_active: bool
    is_staff: bool
    profile: ProfileData
    mypage: MyPageData
    notification: UserNotificationData
    user_plan: UserPlanData


@dataclass(frozen=True, slots=True)
class ProfileData:
    last_name: str
    first_name: str
    gender: str
    birthday: date
    phone: str
    country_code: str
    postal_code: str
    prefecture: str
    city: str
    street: str
    introduction: str


@dataclass(frozen=True, slots=True)
class MyPageData:
    banner: str
    email: str
    content: str
    follower_count: int
    following_count: int
    tag_manager_id: str
    is_advertise: bool


@dataclass(frozen=True, slots=True)
class UserNotificationData:
    is_video: bool
    is_music: bool
    is_comic: bool
    is_picture: bool
    is_blog: bool
    is_chat: bool
    is_follow: bool
    is_reply: bool
    is_like: bool
    is_views: bool


@dataclass(frozen=True, slots=True)
class UserPlanData:
    plan: PlanData
    customer_id: str
    subscription: str
    is_paid: bool
    start_date: date | None
    end_date: date | None
