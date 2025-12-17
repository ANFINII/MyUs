from ninja import Schema


class SettingProfileInData(Schema):
    email: str
    username: str
    nickname: str
    last_name: str
    first_name: str
    gender: str
    year: int
    month: int
    day: int
    phone: str
    postal_code: str
    prefecture: str
    city: str
    street: str
    introduction: str


class SettingMyPageInData(Schema):
    email: str
    tag_manager_id: str
    content: str
    is_advertise: bool


class NotificationInData(Schema):
    is_video: bool
    is_music: bool
    is_comic: bool
    is_picture: bool
    is_blog: bool
    is_chat: bool
    is_follow: bool
    is_reply: bool
    is_like: bool
    is_views: bool
