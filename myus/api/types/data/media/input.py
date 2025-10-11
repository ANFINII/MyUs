from ninja import Schema


class MusicDataIn(Schema):
    title: str
    content: str
    lyric: str
    download: bool
