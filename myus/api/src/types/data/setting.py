from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class SettingProfileData:
    avatar: str
    email: str
    username: str
    nickname: str
    last_name: str
    first_name: str
    year: int
    month: int
    day: int
    gender: str
    phone: str
    country_code: str
    postal_code: str
    prefecture: str
    city: str
    street: str
    introduction: str


@dataclass(frozen=True, slots=True)
class ProfileData:
    last_name: str
    first_name: str
    gender: str
    birthday: date
    phone: str
    postal_code: str
    prefecture: str
    city: str
    street: str
    introduction: str


@dataclass(frozen=True, slots=True)
class SettingMyPageData:
    banner: str
    nickname: str
    email: str
    content: str
    follower_count: int
    following_count: int
    tag_manager_id: str
    plan: str
    plan_start_date: date
    plan_end_date: date
    is_advertise: bool


@dataclass(frozen=True, slots=True)
class MyPageData:
    banner: str
    email: str
    tag_manager_id: str
    content: str
    is_advertise: bool


@dataclass(frozen=True, slots=True)
class SettingNotificationData:
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
