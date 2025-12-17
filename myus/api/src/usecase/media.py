from api.models import Video, Music, Comic, Picture, Blog, Chat
from api.src.domain.media import MediaDomain, FilterOption, SortOption, ExcludeOption
from api.src.types.data.media.index import HomeData, VideoData, MusicData, ComicData, PictureData, BlogData, ChatData
from api.utils.functions.index import create_url
from api.utils.functions.user import get_author

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


def get_videos(limit: int, search: str | None, id: int | None = None) -> list[VideoData]:
    objs = MediaDomain.bulk_get(Video, FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)

    data = [VideoData(
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        image=create_url(obj.image.url),
        video=create_url(obj.video.url),
        convert=create_url(obj.convert.url),
        read=obj.read,
        like_count=obj.total_like(),
        comment_count=obj.comment_count(),
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        author=get_author(obj.author)
    ) for obj in objs]

    return data


def get_musics(limit: int, search: str | None, id: int | None = None) -> list[MusicData]:
    objs = MediaDomain.bulk_get(Music, FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)

    data = [MusicData(
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        lyric=obj.lyric,
        music=create_url(obj.music.url),
        read=obj.read,
        like_count=obj.total_like(),
        comment_count=obj.comment_count(),
        download=obj.download,
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        author=get_author(obj.author)
    ) for obj in objs]

    return data


def get_comics(limit: int, search: str | None, id: int | None = None) -> list[ComicData]:
    objs = MediaDomain.bulk_get(Comic, FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)

    data = [ComicData(
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        image=create_url(obj.image.url),
        read=obj.read,
        like_count=obj.total_like(),
        comment_count=obj.comment_count(),
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        author=get_author(obj.author)
    ) for obj in objs]

    return data


def get_pictures(limit: int, search: str | None, id: int | None = None) -> list[PictureData]:
    objs = MediaDomain.bulk_get(Picture, FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)

    data = [PictureData(
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        image=create_url(obj.image.url),
        read=obj.read,
        like_count=obj.total_like(),
        comment_count=obj.comment_count(),
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        author=get_author(obj.author),
    ) for obj in objs]

    return data


def get_blogs(limit: int, search: str | None, id: int | None = None) -> list[BlogData]:
    objs = MediaDomain.bulk_get(Blog, FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)

    data = [BlogData(
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        image=create_url(obj.image.url),
        read=obj.read,
        like_count=obj.total_like(),
        comment_count=obj.comment_count(),
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        author=get_author(obj.author)
    ) for obj in objs]

    return data


def get_chats(limit: int, search: str | None, id: int | None = None) -> list[ChatData]:
    objs = MediaDomain.bulk_get(Chat, FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)

    data = [ChatData(
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        read=obj.read,
        like_count=obj.total_like(),
        thread=obj.thread_count(),
        joined=obj.joined_count(),
        period=obj.period,
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        author=get_author(obj.author)
    ) for obj in objs]

    return data
