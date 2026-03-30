from dataclasses import dataclass


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
