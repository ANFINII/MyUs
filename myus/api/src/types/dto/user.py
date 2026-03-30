from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UserInData:
    avatar: str | None
    email: str
    username: str
    nickname: str


@dataclass(frozen=True, slots=True)
class AuthorData:
    avatar: str
    ulid: str
    nickname: str
    follower_count: int


@dataclass(frozen=True, slots=True)
class MediaUserData:
    is_like: bool
    is_subscribe: bool


@dataclass(frozen=True, slots=True)
class SearchTagData:
    sequence: int
    name: str


@dataclass(frozen=True, slots=True)
class LikeData:
    is_like: bool
    like_count: int
