from datetime import date
from typing import Annotated
from pydantic import BaseModel, Field
from myus.utils.enum.user import GenderType


class SettingProfileIn(BaseModel):
    email: Annotated[str, Field(max_length=255)]
    username: str
    nickname: Annotated[str, Field(max_length=80)]
    last_name: Annotated[str, Field(max_length=50)]
    first_name: Annotated[str, Field(max_length=50)]
    gender: GenderType
    year: int
    month: int
    day: int
    phone: Annotated[str, Field(max_length=15)]
    postal_code: Annotated[str, Field(max_length=255)]
    prefecture: Annotated[str, Field(max_length=255)]
    city: Annotated[str, Field(max_length=255)]
    street: Annotated[str, Field(max_length=255)]
    introduction: str


class SettingMyPageIn(BaseModel):
    email: Annotated[str, Field(max_length=255)]
    tag_manager_id: Annotated[str, Field(max_length=10)]
    content: str
    is_advertise: bool


class SettingNotificationIn(BaseModel):
    is_video: bool
    is_music: bool
    is_blog: bool
    is_comic: bool
    is_picture: bool
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
    ulid: str
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
    is_blog: bool
    is_comic: bool
    is_picture: bool
    is_chat: bool
    is_follow: bool
    is_reply: bool
    is_like: bool
    is_views: bool
