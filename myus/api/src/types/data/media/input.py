from ninja import Schema


class VideoInData(Schema):
    title: str
    content: str


class MusicInData(Schema):
    title: str
    content: str
    lyric: str
    download: bool


class ComicInData(Schema):
    title: str
    content: str


class PictureInData(Schema):
    title: str
    content: str


class BlogInData(Schema):
    title: str
    content: str
    richtext: str


class ChatInData(Schema):
    title: str
    content: str
    period: str
