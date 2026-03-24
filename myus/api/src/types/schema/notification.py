from pydantic import BaseModel


class NotificationIn(BaseModel):
    ulid: str


class NotificationUserOut(BaseModel):
    avatar: str
    ulid: str
    nickname: str


class NotificationContentOut(BaseModel):
    id: int
    ulid: str
    title: str
    text: str
    read: int


class NotificationItemOut(BaseModel):
    ulid: str
    user_from: NotificationUserOut
    user_to: NotificationUserOut
    type_no: int
    type_name: str
    content_object: NotificationContentOut
    is_confirmed: bool


class NotificationOut(BaseModel):
    count: int
    datas: list[NotificationItemOut]
