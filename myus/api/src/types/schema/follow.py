from pydantic import BaseModel


class FollowIn(BaseModel):
    ulid: str
    is_follow: bool


class FollowUserOut(BaseModel):
    avatar: str
    nickname: str
    introduction: str
    follower_count: int
    following_count: int


class FollowOut(BaseModel):
    is_follow: bool
    follower_count: int
