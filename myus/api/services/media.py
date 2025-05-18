from api.models import Video, Music, Comic, Picture, Blog, Chat
from api.utils.enum.index import MediaModelType
from api.utils.functions.index import create_url
from api.utils.functions.user import get_author
from api.domain.media import MediaDomain, FilterOption, SortOption
from api.types.data.media import HomeData, VideoData, MusicData, ComicData, PictureData, BlogData, ChatData


def get_home(limit: int, search: str | None) -> HomeData:
    data = HomeData(
        videos=get_videos(limit, search),
        musics=get_musics(limit, search),
        comics=get_comics(limit, search),
        pictures=get_pictures(limit, search),
        blogs=get_blogs(limit, search),
        chats=get_chats(limit, search),
    )
    return data


def get_recommend(limit: int, search: str | None) -> HomeData:
    data = HomeData(
        videos=get_videos(limit, search),
        musics=get_musics(limit, search),
        comics=get_comics(limit, search),
        pictures=get_pictures(limit, search),
        blogs=get_blogs(limit, search),
        chats=get_chats(limit, search),
    )
    return data


def get_videos(limit: int, search: str | None) -> list[VideoData]:
    objs = MediaDomain.bulk_get(Video, FilterOption(search=search), SortOption(), limit)

    data = [VideoData(
        id=obj.id,
        title=obj.title,
        content=obj.content,
        image=obj.image.url,
        video=obj.video.url,
        convert=obj.convert.url,
        like=obj.total_like(),
        read=obj.read,
        comment_count=obj.comment_count(),
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        author=get_author(obj.author)
    ) for obj in objs]

    return data


def get_musics(limit: int, search: str | None) -> list[MusicData]:
    objs = MediaDomain.bulk_get(Music, FilterOption(search=search), SortOption(), limit)

    data = [MusicData(
        id=obj.id,
        title=obj.title,
        content=obj.content,
        lyric=obj.lyric,
        music=obj.music.url,
        like=obj.total_like(),
        read=obj.read,
        comment_count=obj.comment_count(),
        download=obj.download,
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        author=get_author(obj.author)
    ) for obj in objs]

    return data


def get_comics(limit: int, search: str | None) -> list[ComicData]:
    objs = MediaDomain.bulk_get(Comic, FilterOption(search=search), SortOption(), limit)

    data = [ComicData(
        id=obj.id,
        title=obj.title,
        content=obj.content,
        image=create_url(obj.image.url),
        like=obj.total_like(),
        read=obj.read,
        comment_count=obj.comment_count(),
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        author=get_author(obj.author)
    ) for obj in objs]

    return data


def get_pictures(limit: int, search: str | None) -> list[PictureData]:
    objs = MediaDomain.bulk_get(Picture, FilterOption(search=search), SortOption(), limit)

    data = [PictureData(
        id=obj.id,
        title=obj.title,
        content=obj.content,
        image=create_url(obj.image.url),
        like=obj.total_like(),
        read=obj.read,
        comment_count=obj.comment_count(),
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        author=get_author(obj.author),
    ) for obj in objs]

    return data


def get_blogs(limit: int, search: str | None) -> list[BlogData]:
    objs = MediaDomain.bulk_get(Blog, FilterOption(search=search), SortOption(), limit)

    data = [BlogData(
        id=obj.id,
        title=obj.title,
        content=obj.content,
        image=create_url(obj.image.url),
        like=obj.total_like(),
        read=obj.read,
        comment_count=obj.comment_count(),
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        author=get_author(obj.author)
    ) for obj in objs]

    return data


def get_chats(limit: int, search: str | None) -> list[ChatData]:
    objs = MediaDomain.bulk_get(Chat, FilterOption(search=search), SortOption(), limit)

    data = [ChatData(
        id=obj.id,
        title=obj.title,
        content=obj.content,
        like=obj.total_like(),
        read=obj.read,
        thread=obj.thread_count(),
        joined=obj.joined_count(),
        period=obj.period,
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        author=get_author(obj.author)
    ) for obj in objs]

    return data
