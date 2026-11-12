from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FollowData:
    id: int
    follower_id: int
    following_id: int
    is_follow: bool
