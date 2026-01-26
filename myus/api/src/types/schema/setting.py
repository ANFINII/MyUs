from datetime import date
from pydantic import BaseModel


class SettingProfileIn(BaseModel):
    email: str
    username: str
    nickname: str
    last_name: str
    first_name: str
    gender: str
    year: int
    month: int
    day: int
    phone: str
    postal_code: str
    prefecture: str
    city: str
    street: str
    introduction: str


class SettingMyPageIn(BaseModel):
    email: str
    tag_manager_id: str
    content: str
    is_advertise: bool


class SettingNotificationIn(BaseModel):
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


class SettingProfileOut(BaseModel):
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


class SettingMyPageOut(BaseModel):
    banner: str
    nickname: str
    email: str
    content: str
    follower_count: int
    following_count: int
    tag_manager_id: str
    plan: str
    plan_start_date: date | None
    plan_end_date: date | None
    is_advertise: bool


class SettingNotificationOut(BaseModel):
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
