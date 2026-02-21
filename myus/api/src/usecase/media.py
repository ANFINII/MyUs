from dataclasses import replace
from datetime import date, datetime
from django.http import HttpRequest
from ninja import UploadedFile
from api.db.models.media import Blog, Chat, Comic, Music, Picture, Video
from api.src.domain.interface.media.video.data import VideoData
from api.src.domain.interface.media.music.data import MusicData
from api.src.domain.interface.media.comic.data import ComicData
from api.src.domain.interface.media.picture.data import PictureData
from api.src.domain.interface.media.blog.data import BlogData
from api.src.domain.interface.media.chat.data import ChatData
from api.src.domain.interface.media.data import HomeData, MediaCreateData, HashtagData
from api.src.domain.interface.media.video.interface import VideoInterface
from api.src.domain.interface.media.music.interface import MusicInterface
from api.src.domain.interface.media.comic.interface import ComicInterface
from api.src.domain.interface.media.picture.interface import PictureInterface
from api.src.domain.interface.media.blog.interface import BlogInterface
from api.src.domain.interface.media.chat.interface import ChatInterface
from api.src.domain.interface.channel.data import ChannelData
from api.src.domain.entity.media.video.repository import VideoRepository
from api.src.domain.entity.media.music.repository import MusicRepository
from api.src.domain.entity.media.comic.repository import ComicRepository
from api.src.domain.entity.media.picture.repository import PictureRepository
from api.src.domain.entity.media.blog.repository import BlogRepository
from api.src.domain.entity.media.chat.repository import ChatRepository
from api.src.domain.interface.media.index import FilterOption, SortOption, ExcludeOption
from api.src.injectors.container import injector
from api.src.types.data.media import VideoDetailData, MusicDetailData, ComicDetailData, PictureDetailData, BlogDetailData, ChatDetailData
from api.src.types.schema.media import VideoIn, MusicIn, ComicIn, PictureIn, BlogIn, ChatIn
from api.src.usecase.auth import auth_check
from api.src.usecase.comment import get_comments
from api.src.usecase.message import get_messages
from api.utils.enum.index import CommentType
from api.utils.functions.index import create_url
from api.utils.functions.map import comment_type_no_map
from api.utils.functions.user import get_media_user


def create_video(channel: ChannelData, input: VideoIn, image: UploadedFile, video: UploadedFile, convert: UploadedFile) -> MediaCreateData:
    repository = injector.get(VideoInterface)

    new_video = VideoData(
        id=0,
        ulid="",
        title=input.title,
        content=input.content,
        image=image.name or "",
        video=video.name or "",
        convert=convert.name or "",
        read=0,
        publish=True,
        created=datetime.min,
        updated=datetime.min,
        like_count=0,
        comment_count=0,
        channel=channel,
    )

    repository.bulk_save([new_video])
    return MediaCreateData(ulid="")


def create_music(channel: ChannelData, input: MusicIn, music: UploadedFile) -> MediaCreateData:
    repository = injector.get(MusicInterface)

    new_music = MusicData(
        id=0,
        ulid="",
        title=input.title,
        content=input.content,
        lyric=input.lyric,
        music=music.name or "",
        read=0,
        download=input.download,
        publish=True,
        created=datetime.min,
        updated=datetime.min,
        like_count=0,
        comment_count=0,
        channel=channel,
    )

    repository.bulk_save([new_music])
    return MediaCreateData(ulid="")


def create_comic(channel: ChannelData, input: ComicIn, image: UploadedFile) -> MediaCreateData:
    repository = injector.get(ComicInterface)

    new_comic = ComicData(
        id=0,
        ulid="",
        title=input.title,
        content=input.content,
        image=image.name or "",
        read=0,
        publish=True,
        created=datetime.min,
        updated=datetime.min,
        like_count=0,
        comment_count=0,
        channel=channel,
    )

    repository.bulk_save([new_comic])
    return MediaCreateData(ulid="")


def create_picture(channel: ChannelData, input: PictureIn, image: UploadedFile) -> MediaCreateData:
    repository = injector.get(PictureInterface)

    new_picture = PictureData(
        id=0,
        ulid="",
        title=input.title,
        content=input.content,
        image=image.name or "",
        read=0,
        publish=True,
        created=datetime.min,
        updated=datetime.min,
        like_count=0,
        comment_count=0,
        channel=channel,
    )

    repository.bulk_save([new_picture])
    return MediaCreateData(ulid="")


def create_blog(channel: ChannelData, input: BlogIn, image: UploadedFile) -> MediaCreateData:
    repository = injector.get(BlogInterface)

    new_blog = BlogData(
        id=0,
        ulid="",
        title=input.title,
        content=input.content,
        richtext=input.richtext,
        delta="",
        image=image.name or "",
        read=0,
        publish=True,
        created=datetime.min,
        updated=datetime.min,
        like_count=0,
        comment_count=0,
        channel=channel,
    )

    repository.bulk_save([new_blog])
    return MediaCreateData(ulid="")


def create_chat(channel: ChannelData, input: ChatIn) -> MediaCreateData:
    repository = injector.get(ChatInterface)

    new_chat = ChatData(
        id=0,
        ulid="",
        title=input.title,
        content=input.content,
        read=0,
        period=date.fromisoformat(input.period),
        publish=True,
        created=datetime.min,
        updated=datetime.min,
        like_count=0,
        thread_count=0,
        joined_count=0,
        channel=channel,
    )

    repository.bulk_save([new_chat])
    return MediaCreateData(ulid="")


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
    repository = VideoRepository()
    ids = repository.get_ids(FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)
    objs = repository.bulk_get(ids=ids)

    data = [replace(o,
        image=create_url(o.image),
        video=create_url(o.video),
        convert=create_url(o.convert),
    ) for o in objs]

    return data


def get_musics(limit: int, search: str, id: int | None = None) -> list[MusicData]:
    repository = MusicRepository()
    ids = repository.get_ids(FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)
    objs = repository.bulk_get(ids=ids)
    data = [replace(o, music=create_url(o.music)) for o in objs]
    return data


def get_comics(limit: int, search: str, id: int | None = None) -> list[ComicData]:
    repository = ComicRepository()
    ids = repository.get_ids(FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)
    objs = repository.bulk_get(ids=ids)
    data = [replace(o, image=create_url(o.image)) for o in objs]
    return data


def get_pictures(limit: int, search: str, id: int | None = None) -> list[PictureData]:
    repository = PictureRepository()
    ids = repository.get_ids(FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)
    objs = repository.bulk_get(ids=ids)
    data = [replace(o, image=create_url(o.image)) for o in objs]
    return data


def get_blogs(limit: int, search: str, id: int | None = None) -> list[BlogData]:
    repository = BlogRepository()
    ids = repository.get_ids(FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)
    objs = repository.bulk_get(ids=ids)
    data = [replace(o, image=create_url(o.image)) for o in objs]
    return data


def get_chats(limit: int, search: str, id: int | None = None) -> list[ChatData]:
    repository = ChatRepository()
    ids = repository.get_ids(FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)
    objs = repository.bulk_get(ids=ids)
    return objs


def get_video_detail(request: HttpRequest, ulid: str, publish: bool = True) -> VideoDetailData | None:
    repository = VideoRepository()
    ids = repository.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption())
    entities = repository.bulk_get(ids=ids)
    e = entities[0] if len(entities) > 0 else None
    if e is None:
        return None

    user_id = auth_check(request)
    type_no = comment_type_no_map(CommentType.VIDEO)
    comments = get_comments(type_no=type_no, object_id=e.id, user_id=user_id)

    obj = Video.objects.prefetch_related("hashtag", "like").get(id=e.id)

    data = VideoDetailData(
        id=e.id,
        ulid=e.ulid,
        title=e.title,
        content=e.content,
        image=create_url(e.image),
        video=create_url(e.video),
        convert=create_url(e.convert),
        comments=comments,
        hashtags=[HashtagData(jp_name=h.jp_name) for h in obj.hashtag.all()],
        read=e.read,
        like_count=e.like_count,
        publish=e.publish,
        created=e.created,
        updated=e.updated,
        channel=e.channel,
        mediaUser=get_media_user(obj, user_id),
    )

    return data


def get_music_detail(request: HttpRequest, ulid: str, publish: bool = True) -> MusicDetailData | None:
    repository = MusicRepository()
    ids = repository.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption())
    entities = repository.bulk_get(ids=ids)
    e = entities[0] if len(entities) > 0 else None
    if e is None:
        return None

    user_id = auth_check(request)
    type_no = comment_type_no_map(CommentType.MUSIC)
    comments = get_comments(type_no=type_no, object_id=e.id, user_id=user_id)

    obj = Music.objects.prefetch_related("hashtag", "like").get(id=e.id)

    data = MusicDetailData(
        id=e.id,
        ulid=e.ulid,
        title=e.title,
        content=e.content,
        lyric=e.lyric,
        music=create_url(e.music),
        download=e.download,
        comments=comments,
        hashtags=[HashtagData(jp_name=h.jp_name) for h in obj.hashtag.all()],
        read=e.read,
        like_count=e.like_count,
        publish=e.publish,
        created=e.created,
        updated=e.updated,
        channel=e.channel,
        mediaUser=get_media_user(obj, user_id),
    )

    return data


def get_comic_detail(request: HttpRequest, ulid: str, publish: bool = True) -> ComicDetailData | None:
    repository = ComicRepository()
    ids = repository.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption())
    entities = repository.bulk_get(ids=ids)
    e = entities[0] if len(entities) > 0 else None
    if e is None:
        return None

    user_id = auth_check(request)
    type_no = comment_type_no_map(CommentType.COMIC)
    comments = get_comments(type_no=type_no, object_id=e.id, user_id=user_id)

    obj = Comic.objects.prefetch_related("hashtag", "like").get(id=e.id)

    data = ComicDetailData(
        id=e.id,
        ulid=e.ulid,
        title=e.title,
        content=e.content,
        image=create_url(e.image),
        comments=comments,
        hashtags=[HashtagData(jp_name=h.jp_name) for h in obj.hashtag.all()],
        read=e.read,
        like_count=e.like_count,
        publish=e.publish,
        created=e.created,
        updated=e.updated,
        channel=e.channel,
        mediaUser=get_media_user(obj, user_id),
    )

    return data


def get_blog_detail(request: HttpRequest, ulid: str, publish: bool = True) -> BlogDetailData | None:
    repository = BlogRepository()
    ids = repository.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption())
    entities = repository.bulk_get(ids=ids)
    e = entities[0] if len(entities) > 0 else None
    if e is None:
        return None

    user_id = auth_check(request)
    type_no = comment_type_no_map(CommentType.BLOG)
    comments = get_comments(type_no=type_no, object_id=e.id, user_id=user_id)

    obj = Blog.objects.prefetch_related("hashtag", "like").get(id=e.id)

    data = BlogDetailData(
        id=e.id,
        ulid=e.ulid,
        title=e.title,
        content=e.content,
        richtext=e.richtext,
        image=create_url(e.image),
        comments=comments,
        hashtags=[HashtagData(jp_name=h.jp_name) for h in obj.hashtag.all()],
        read=e.read,
        like_count=e.like_count,
        publish=e.publish,
        created=e.created,
        updated=e.updated,
        channel=e.channel,
        mediaUser=get_media_user(obj, user_id),
    )

    return data


def get_picture_detail(request: HttpRequest, ulid: str, publish: bool = True) -> PictureDetailData | None:
    repository = PictureRepository()
    ids = repository.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption())
    entities = repository.bulk_get(ids=ids)
    e = entities[0] if len(entities) > 0 else None
    if e is None:
        return None

    user_id = auth_check(request)
    type_no = comment_type_no_map(CommentType.PICTURE)
    comments = get_comments(type_no=type_no, object_id=e.id, user_id=None)

    obj = Picture.objects.prefetch_related("hashtag", "like").get(id=e.id)

    data = PictureDetailData(
        id=e.id,
        ulid=e.ulid,
        title=e.title,
        content=e.content,
        image=create_url(e.image),
        comments=comments,
        hashtags=[HashtagData(jp_name=h.jp_name) for h in obj.hashtag.all()],
        read=e.read,
        like_count=e.like_count,
        publish=e.publish,
        created=e.created,
        updated=e.updated,
        channel=e.channel,
        mediaUser=get_media_user(obj, user_id),
    )

    return data


def get_chat_detail(request: HttpRequest, ulid: str, publish: bool = True) -> ChatDetailData | None:
    repository = ChatRepository()
    ids = repository.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption())
    entities = repository.bulk_get(ids=ids)
    e = entities[0] if len(entities) > 0 else None
    if e is None:
        return None

    user_id = auth_check(request)
    messages = get_messages(chat_id=e.id)
    obj = Chat.objects.prefetch_related("hashtag", "like").get(id=e.id)

    data = ChatDetailData(
        id=e.id,
        ulid=e.ulid,
        title=e.title,
        content=e.content,
        messages=messages,
        hashtags=[HashtagData(jp_name=h.jp_name) for h in obj.hashtag.all()],
        read=e.read,
        like_count=e.like_count,
        thread=e.thread_count,
        joined=e.joined_count,
        period=e.period,
        publish=e.publish,
        created=e.created,
        updated=e.updated,
        channel=e.channel,
        mediaUser=get_media_user(obj, user_id),
    )

    return data
