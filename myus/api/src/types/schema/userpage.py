from datetime import datetime
from pydantic import BaseModel
from api.src.types.schema.channel import ChannelOut
from api.src.types.schema.media.output import VideoOut, MusicOut, BlogOut, ComicOut, PictureOut, ChatOut


class UserPageOut(BaseModel):
    avatar: str
    banner: str
    nickname: str
    email: str
    content: str
    date_joined: datetime
    follower_count: int
    following_count: int
    is_follow: bool
    channels: list[ChannelOut]


class UserPageMediaOut(BaseModel):
    videos: list[VideoOut]
    musics: list[MusicOut]
    blogs: list[BlogOut]
    comics: list[ComicOut]
    pictures: list[PictureOut]
    chats: list[ChatOut]
