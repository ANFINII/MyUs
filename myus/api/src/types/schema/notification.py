from pydantic import BaseModel


class NotificationUserOut(BaseModel):
    avatar: str
    nickname: str


class NotificationContentOut(BaseModel):
    id: int


class NotificationItemOut(BaseModel):
    id: int
    user_from: NotificationUserOut
    user_to: NotificationUserOut
    type_no: int
    type_name: str
    content_object: NotificationContentOut
    is_confirmed: bool


class NotificationOut(BaseModel):
    count: int
    datas: list[NotificationItemOut]
