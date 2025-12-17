from ninja import Schema


class FollowInData(Schema):
    ulid: str
    is_follow: bool
