from django.http import HttpRequest
from ninja import UploadedFile

from api.db.models.channel import Channel
from api.src.domain.media.index import FilterOption, SortOption, ExcludeOption
from api.src.domain.media.video import VideoDomain
from api.src.domain.media.music import MusicDomain
from api.src.domain.media.comic import ComicDomain
from api.src.domain.media.picture import PictureDomain
from api.src.domain.media.blog import BlogDomain
from api.src.domain.media.chat import ChatDomain
from api.src.types.data.media import HomeData, MediaCreateData, VideoData, MusicData, ComicData, PictureData, BlogData, ChatData
from api.src.types.data.media import VideoDetailData, MusicDetailData, ComicDetailData, PictureDetailData, BlogDetailData, ChatDetailData, HashtagData
from api.src.usecase.comment import get_comments
from api.src.usecase.message import get_messages
from api.src.usecase.user import get_user
from api.utils.enum.index import CommentType
from api.utils.functions.index import create_url
from api.utils.functions.map import comment_type_no_map
from api.utils.functions.user import get_author, get_media_user


def create_video(channel: Channel, title: str, content: str, image: UploadedFile, video: UploadedFile, convert: UploadedFile) -> MediaCreateData:
    obj = VideoDomain.create(channel=channel, title=title, content=content, image=image, video=video, convert=convert)
    return MediaCreateData(ulid=str(obj.ulid))


def create_music(channel: Channel, title: str, content: str, lyric: str, download: bool, music: UploadedFile) -> MediaCreateData:
    obj = MusicDomain.create(channel=channel, title=title, content=content, lyric=lyric, download=download, music=music)
    return MediaCreateData(ulid=str(obj.ulid))


def create_comic(channel: Channel, title: str, content: str, image: UploadedFile) -> MediaCreateData:
    obj = ComicDomain.create(channel=channel, title=title, content=content, image=image)
    return MediaCreateData(ulid=str(obj.ulid))


def create_picture(channel: Channel, title: str, content: str, image: UploadedFile) -> MediaCreateData:
    obj = PictureDomain.create(channel=channel, title=title, content=content, image=image)
    return MediaCreateData(ulid=str(obj.ulid))


def create_blog(channel: Channel, title: str, content: str, richtext: str, image: UploadedFile) -> MediaCreateData:
    obj = BlogDomain.create(channel=channel, title=title, content=content, richtext=richtext, image=image)
    return MediaCreateData(ulid=str(obj.ulid))


def create_chat(channel: Channel, title: str, content: str, period: str) -> MediaCreateData:
    obj = ChatDomain.create(channel=channel, title=title, content=content, period=period)
    return MediaCreateData(ulid=str(obj.ulid))


def get_home(limit: int, search: str) -> HomeData:
    data = HomeData(
        videos=get_videos(limit, search),
        musics=get_musics(limit, search),
        comics=get_comics(limit, search),
        pictures=get_pictures(limit, search),
        blogs=get_blogs(limit, search),
        chats=get_chats(limit, search),
    )
    return data


def get_recommend(limit: int, search: str) -> HomeData:
    data = HomeData(
        videos=get_videos(limit, search),
        musics=get_musics(limit, search),
        comics=get_comics(limit, search),
        pictures=get_pictures(limit, search),
        blogs=get_blogs(limit, search),
        chats=get_chats(limit, search),
    )
    return data


def get_videos(limit: int, search: str, id: int | None = None) -> list[VideoData]:
    ids = VideoDomain.get_ids(FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)
    objs = VideoDomain.bulk_get(ids=ids)

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
        author=get_author(obj.channel.owner)
    ) for obj in objs]

    return data


def get_musics(limit: int, search: str, id: int | None = None) -> list[MusicData]:
    ids = MusicDomain.get_ids(FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)
    objs = MusicDomain.bulk_get(ids=ids)

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
        author=get_author(obj.channel.owner)
    ) for obj in objs]

    return data


def get_comics(limit: int, search: str, id: int | None = None) -> list[ComicData]:
    ids = ComicDomain.get_ids(FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)
    objs = ComicDomain.bulk_get(ids=ids)

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
        author=get_author(obj.channel.owner)
    ) for obj in objs]

    return data


def get_pictures(limit: int, search: str, id: int | None = None) -> list[PictureData]:
    ids = PictureDomain.get_ids(FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)
    objs = PictureDomain.bulk_get(ids=ids)

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
        author=get_author(obj.channel.owner),
    ) for obj in objs]

    return data


def get_blogs(limit: int, search: str, id: int | None = None) -> list[BlogData]:
    ids = BlogDomain.get_ids(FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)
    objs = BlogDomain.bulk_get(ids=ids)

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
        author=get_author(obj.channel.owner)
    ) for obj in objs]

    return data


def get_chats(limit: int, search: str, id: int | None = None) -> list[ChatData]:
    ids = ChatDomain.get_ids(FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)
    objs = ChatDomain.bulk_get(ids=ids)

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
        author=get_author(obj.channel.owner)
    ) for obj in objs]

    return data


def get_video_detail(request: HttpRequest, ulid: str, publish: bool = True) -> VideoDetailData | None:
    ids = VideoDomain.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption())
    objs = VideoDomain.bulk_get(ids=ids)
    obj = objs[0] if objs else None
    if obj is None:
        return None

    user = get_user(request)
    user_id = user.id if user else None
    type_no = comment_type_no_map(CommentType.VIDEO)
    comments = get_comments(type_no=type_no, object_id=obj.id, user_id=user_id)

    data = VideoDetailData(
        id=obj.id,
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        image=create_url(obj.image.url),
        video=create_url(obj.video.url),
        convert=create_url(obj.convert.url),
        comments=comments,
        hashtags=[HashtagData(jp_name=hashtag.jp_name) for hashtag in obj.hashtag.all()],
        read=obj.read,
        like_count=obj.total_like(),
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        author=get_author(obj.channel.owner),
        mediaUser=get_media_user(obj, user),
    )

    return data


def get_music_detail(request: HttpRequest, ulid: str, publish: bool = True) -> MusicDetailData | None:
    ids = MusicDomain.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption())
    objs = MusicDomain.bulk_get(ids=ids)
    obj = objs[0] if objs else None
    if obj is None:
        return None

    user = get_user(request)
    user_id = user.id if user else None
    type_no = comment_type_no_map(CommentType.MUSIC)
    comments = get_comments(type_no=type_no, object_id=obj.id, user_id=user_id)

    data = MusicDetailData(
        id=obj.id,
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        lyric=obj.lyric,
        music=create_url(obj.music.url),
        download=obj.download,
        comments=comments,
        hashtags=[HashtagData(jp_name=hashtag.jp_name) for hashtag in obj.hashtag.all()],
        read=obj.read,
        like_count=obj.total_like(),
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        author=get_author(obj.channel.owner),
        mediaUser=get_media_user(obj, user),
    )

    return data


def get_comic_detail(request: HttpRequest, ulid: str, publish: bool = True) -> ComicDetailData | None:
    ids = ComicDomain.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption())
    objs = ComicDomain.bulk_get(ids=ids)
    obj = objs[0] if objs else None
    if obj is None:
        return None

    user = get_user(request)
    user_id = user.id if user else None
    type_no = comment_type_no_map(CommentType.COMIC)
    comments = get_comments(type_no=type_no, object_id=obj.id, user_id=user_id)

    data = ComicDetailData(
        id=obj.id,
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        image=create_url(obj.image.url),
        comments=comments,
        hashtags=[HashtagData(jp_name=hashtag.jp_name) for hashtag in obj.hashtag.all()],
        read=obj.read,
        like_count=obj.total_like(),
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        author=get_author(obj.channel.owner),
        mediaUser=get_media_user(obj, user),
    )

    return data


def get_blog_detail(request: HttpRequest, ulid: str, publish: bool = True) -> BlogDetailData | None:
    ids = BlogDomain.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption())
    objs = BlogDomain.bulk_get(ids=ids)
    obj = objs[0] if objs else None
    if obj is None:
        return None

    user = get_user(request)
    user_id = user.id if user else None
    type_no = comment_type_no_map(CommentType.BLOG)
    comments = get_comments(type_no=type_no, object_id=obj.id, user_id=user_id)

    data = BlogDetailData(
        id=obj.id,
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        richtext=obj.richtext,
        image=create_url(obj.image.url),
        comments=comments,
        hashtags=[HashtagData(jp_name=hashtag.jp_name) for hashtag in obj.hashtag.all()],
        read=obj.read,
        like_count=obj.total_like(),
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        author=get_author(obj.channel.owner),
        mediaUser=get_media_user(obj, user),
    )

    return data


def get_picture_detail(request: HttpRequest, ulid: str, publish: bool = True) -> PictureDetailData | None:
    ids = PictureDomain.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption())
    objs = PictureDomain.bulk_get(ids=ids)
    obj = objs[0] if objs else None
    if obj is None:
        return None

    user = get_user(request)
    user_id = user.id if user else None
    type_no = comment_type_no_map(CommentType.PICTURE)
    comments = get_comments(type_no=type_no, object_id=obj.id, user_id=user_id)

    data = PictureDetailData(
        id=obj.id,
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        image=create_url(obj.image.url),
        comments=comments,
        hashtags=[HashtagData(jp_name=hashtag.jp_name) for hashtag in obj.hashtag.all()],
        read=obj.read,
        like_count=obj.total_like(),
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        author=get_author(obj.channel.owner),
        mediaUser=get_media_user(obj, user),
    )

    return data

def get_chat_detail(request: HttpRequest, ulid: str, publish: bool = True) -> ChatDetailData | None:
    ids = ChatDomain.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption())
    objs = ChatDomain.bulk_get(ids=ids)
    obj = objs[0] if objs else None
    if obj is None:
        return None

    user = get_user(request)
    messages = get_messages(chat_id=obj.id)

    data = ChatDetailData(
        id=obj.id,
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        messages=messages,
        hashtags=[HashtagData(jp_name=hashtag.jp_name) for hashtag in obj.hashtag.all()],
        read=obj.read,
        like_count=obj.total_like(),
        thread=obj.thread_count(),
        joined=obj.joined_count(),
        period=obj.period,
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        author=get_author(obj.channel.owner),
        mediaUser=get_media_user(obj, user),
    )

    return data
