from ninja import Schema


class VideoDataIn(Schema):
    title: str
    content: str


class MusicDataIn(Schema):
    title: str
    content: str
    lyric: str
    download: bool


class ComicDataIn(Schema):
    title: str
    content: str


class PictureDataIn(Schema):
    title: str
    content: str


class BlogDataIn(Schema):
    title: str
    content: str
    richtext: str


class ChatDataIn(Schema):
    title: str
    content: str
    period: str
