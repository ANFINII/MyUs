from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class FollowUserData:
    avatar: str
    nickname: str
    introduction: str
    follower_count: int
    following_count: int


@dataclass(frozen=True, slots=True)
class FollowData:
    id: int
    follower: FollowUserData
    following: FollowUserData
    created: datetime
    is_follow: bool


@dataclass(frozen=True, slots=True)
class FollowCreateData:
    follower_id: int
    following_id: int
    is_follow: bool


@dataclass(frozen=True, slots=True)
class FollowOutData:
    is_follow: bool
    follower_count: int
