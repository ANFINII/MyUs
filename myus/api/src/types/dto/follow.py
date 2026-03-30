from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class FollowUserDTO:
    avatar: str
    nickname: str
    introduction: str
    follower_count: int
    following_count: int


@dataclass(frozen=True, slots=True)
class FollowDTO:
    id: int
    follower: FollowUserDTO
    following: FollowUserDTO
    created: datetime
    is_follow: bool



@dataclass(frozen=True, slots=True)
class FollowOutDTO:
    is_follow: bool
    follower_count: int
