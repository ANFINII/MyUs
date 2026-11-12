from dataclasses import dataclass
from myus.utils.enum.user import GenderType


@dataclass(frozen=True, slots=True)
class AuthorDTO:
    avatar: str
    ulid: str
    nickname: str
    follower_count: int


@dataclass(frozen=True, slots=True)
class MediaUserDTO:
    is_like: bool
    is_subscribe: bool


@dataclass(frozen=True, slots=True)
class LikeDTO:
    is_like: bool
    like_count: int


@dataclass(frozen=True, slots=True)
class SignupInDTO:
    token: str
    email: str
    username: str
    nickname: str
    password1: str
    password2: str
    last_name: str
    first_name: str
    year: int
    month: int
    day: int
    gender: GenderType


@dataclass(frozen=True, slots=True)
class PasswordChangeInDTO:
    old_password: str
    password1: str
    password2: str


@dataclass(frozen=True, slots=True)
class PasswordResetInDTO:
    token: str
    password1: str
    password2: str


@dataclass(frozen=True, slots=True)
class SettingProfileUpdateDTO:
    email: str
    username: str
    nickname: str
    last_name: str
    first_name: str
    gender: GenderType
    year: int
    month: int
    day: int
    phone: str
    postal_code: str
    prefecture: str
    city: str
    street: str
    introduction: str


@dataclass(frozen=True, slots=True)
class SettingMyPageUpdateDTO:
    email: str
    tag_manager_id: str
    content: str
    is_advertise: bool


@dataclass(frozen=True, slots=True)
class SettingNotificationUpdateDTO:
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


@dataclass(frozen=True, slots=True)
class SearchTagUpdateDTO:
    sequence: int
    name: str
