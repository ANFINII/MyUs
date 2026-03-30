from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FollowUserDTO:
    avatar: str
    nickname: str
    introduction: str
    follower_count: int
    following_count: int


@dataclass(frozen=True, slots=True)
class FollowDTO:
    is_follow: bool
    follower_count: int
