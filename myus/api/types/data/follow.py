from datetime import datetime
from dataclasses import dataclass
from ninja import Schema


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
class FollowInData:
    follower_id: int
    following_id: int


@dataclass(frozen=True, slots=True)
class FollowOutData:
    is_follow: bool
    follower_count: int


class FollowInData(Schema):
    ulid: str
    is_follow: bool


@dataclass(frozen=True, slots=True)
class SearchTagData:
    sequence: int
    name: str
