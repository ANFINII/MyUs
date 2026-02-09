from django.http import HttpRequest
from ninja import UploadedFile
from api.db.models.channel import Channel
from api.db.models.media import Blog, Chat, Comic, Music, Picture, Video
from api.src.domain.entity.media.video.repository import VideoRepository
from api.src.domain.entity.media.music.repository import MusicRepository
from api.src.domain.entity.media.comic.repository import ComicRepository
from api.src.domain.entity.media.picture.repository import PictureRepository
from api.src.domain.entity.media.blog.repository import BlogRepository
from api.src.domain.entity.media.chat.repository import ChatRepository
from api.src.domain.entity.user.repository import UserRepository
from api.src.domain.interface.media.index import FilterOption, SortOption, ExcludeOption
from api.src.domain.interface.user.data import UserAllData
from api.src.types.data.media import HomeData, MediaCreateData, VideoData, MusicData, ComicData, PictureData, BlogData, ChatData
from api.src.types.data.media import VideoDetailData, MusicDetailData, ComicDetailData, PictureDetailData, BlogDetailData, ChatDetailData, HashtagData
from api.src.types.data.user import AuthorData
from api.src.usecase.auth import auth_check
from api.src.usecase.comment import get_comments
from api.src.usecase.message import get_messages
from api.utils.enum.index import CommentType
from api.utils.functions.index import create_url
from api.utils.functions.map import comment_type_no_map
from api.utils.functions.user import get_media_user


def _build_user_map(owner_ids: list[int]) -> dict[int, UserAllData]:
    if len(owner_ids) == 0:
        return {}
    user_repo = UserRepository()
    users = user_repo.bulk_get(list(set(owner_ids)))
    return {u.user.id: u for u in users}


def _to_author(user_map: dict[int, UserAllData], owner_id: int) -> AuthorData:
    user_all = user_map.get(owner_id)
    if user_all is None:
        return AuthorData(avatar="", ulid="", nickname="", follower_count=0)
    return _build_author(user_all)


def _build_author(user_all: UserAllData) -> AuthorData:
    return AuthorData(
        avatar=create_url(user_all.user.avatar),
        ulid=user_all.user.ulid,
        nickname=user_all.user.nickname,
        follower_count=user_all.mypage.follower_count,
    )


def create_video(channel: Channel, title: str, content: str, image: UploadedFile, video: UploadedFile, convert: UploadedFile) -> MediaCreateData:
    repository = VideoRepository()
    data = repository.create(channel=channel, title=title, content=content, image=image, video=video, convert=convert)
    return MediaCreateData(ulid=data.ulid)


def create_music(channel: Channel, title: str, content: str, lyric: str, download: bool, music: UploadedFile) -> MediaCreateData:
    repository = MusicRepository()
    data = repository.create(channel=channel, title=title, content=content, lyric=lyric, download=download, music=music)
    return MediaCreateData(ulid=data.ulid)


def create_comic(channel: Channel, title: str, content: str, image: UploadedFile) -> MediaCreateData:
    repository = ComicRepository()
    data = repository.create(channel=channel, title=title, content=content, image=image)
    return MediaCreateData(ulid=data.ulid)


def create_picture(channel: Channel, title: str, content: str, image: UploadedFile) -> MediaCreateData:
    repository = PictureRepository()
    data = repository.create(channel=channel, title=title, content=content, image=image)
    return MediaCreateData(ulid=data.ulid)


def create_blog(channel: Channel, title: str, content: str, richtext: str, image: UploadedFile) -> MediaCreateData:
    repository = BlogRepository()
    data = repository.create(channel=channel, title=title, content=content, richtext=richtext, image=image)
    return MediaCreateData(ulid=data.ulid)


def create_chat(channel: Channel, title: str, content: str, period: str) -> MediaCreateData:
    repository = ChatRepository()
    data = repository.create(channel=channel, title=title, content=content, period=period)
    return MediaCreateData(ulid=data.ulid)


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
    entities = repository.bulk_get(ids=ids)
    user_map = _build_user_map([e.owner_id for e in entities])

    data = [VideoData(
        ulid=e.ulid,
        title=e.title,
        content=e.content,
        image=create_url(e.image),
        video=create_url(e.video),
        convert=create_url(e.convert),
        read=e.read,
        like_count=e.like_count,
        comment_count=e.comment_count,
        publish=e.publish,
        created=e.created,
        updated=e.updated,
        author=_to_author(user_map, e.owner_id),
    ) for e in entities]

    return data


def get_musics(limit: int, search: str, id: int | None = None) -> list[MusicData]:
    repository = MusicRepository()
    ids = repository.get_ids(FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)
    entities = repository.bulk_get(ids=ids)
    user_map = _build_user_map([e.owner_id for e in entities])

    data = [MusicData(
        ulid=e.ulid,
        title=e.title,
        content=e.content,
        lyric=e.lyric,
        music=create_url(e.music),
        read=e.read,
        like_count=e.like_count,
        comment_count=e.comment_count,
        download=e.download,
        publish=e.publish,
        created=e.created,
        updated=e.updated,
        author=_to_author(user_map, e.owner_id),
    ) for e in entities]

    return data


def get_comics(limit: int, search: str, id: int | None = None) -> list[ComicData]:
    repository = ComicRepository()
    ids = repository.get_ids(FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)
    entities = repository.bulk_get(ids=ids)
    user_map = _build_user_map([e.owner_id for e in entities])

    data = [ComicData(
        ulid=e.ulid,
        title=e.title,
        content=e.content,
        image=create_url(e.image),
        read=e.read,
        like_count=e.like_count,
        comment_count=e.comment_count,
        publish=e.publish,
        created=e.created,
        updated=e.updated,
        author=_to_author(user_map, e.owner_id),
    ) for e in entities]

    return data


def get_pictures(limit: int, search: str, id: int | None = None) -> list[PictureData]:
    repository = PictureRepository()
    ids = repository.get_ids(FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)
    entities = repository.bulk_get(ids=ids)
    user_map = _build_user_map([e.owner_id for e in entities])

    data = [PictureData(
        ulid=e.ulid,
        title=e.title,
        content=e.content,
        image=create_url(e.image),
        read=e.read,
        like_count=e.like_count,
        comment_count=e.comment_count,
        publish=e.publish,
        created=e.created,
        updated=e.updated,
        author=_to_author(user_map, e.owner_id),
    ) for e in entities]

    return data


def get_blogs(limit: int, search: str, id: int | None = None) -> list[BlogData]:
    repository = BlogRepository()
    ids = repository.get_ids(FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)
    entities = repository.bulk_get(ids=ids)
    user_map = _build_user_map([e.owner_id for e in entities])

    data = [BlogData(
        ulid=e.ulid,
        title=e.title,
        content=e.content,
        image=create_url(e.image),
        read=e.read,
        like_count=e.like_count,
        comment_count=e.comment_count,
        publish=e.publish,
        created=e.created,
        updated=e.updated,
        author=_to_author(user_map, e.owner_id),
    ) for e in entities]

    return data


def get_chats(limit: int, search: str, id: int | None = None) -> list[ChatData]:
    repository = ChatRepository()
    ids = repository.get_ids(FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)
    entities = repository.bulk_get(ids=ids)
    user_map = _build_user_map([e.owner_id for e in entities])

    data = [ChatData(
        ulid=e.ulid,
        title=e.title,
        content=e.content,
        read=e.read,
        like_count=e.like_count,
        thread=e.thread_count,
        joined=e.joined_count,
        period=e.period,
        publish=e.publish,
        created=e.created,
        updated=e.updated,
        author=_to_author(user_map, e.owner_id),
    ) for e in entities]

    return data


def get_video_detail(request: HttpRequest, ulid: str, publish: bool = True) -> VideoDetailData | None:
    repository = VideoRepository()
    ids = repository.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption())
    entities = repository.bulk_get(ids=ids)
    e = entities[0] if len(entities) > 0 else None
    if e is None:
        return None

    user_id = auth_check(request)
    user_map = _build_user_map([e.owner_id])
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
        author=_to_author(user_map, e.owner_id),
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
    user_map = _build_user_map([e.owner_id])
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
        author=_to_author(user_map, e.owner_id),
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
    user_map = _build_user_map([e.owner_id])
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
        author=_to_author(user_map, e.owner_id),
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
    user_map = _build_user_map([e.owner_id])
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
        author=_to_author(user_map, e.owner_id),
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
    user_map = _build_user_map([e.owner_id])
    type_no = comment_type_no_map(CommentType.PICTURE)
    comments = get_comments(type_no=type_no, object_id=e.id, user_id=user_id)

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
        author=_to_author(user_map, e.owner_id),
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
    user_map = _build_user_map([e.owner_id])
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
        author=_to_author(user_map, e.owner_id),
        mediaUser=get_media_user(obj, user_id),
    )

    return data
