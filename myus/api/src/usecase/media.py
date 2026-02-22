from dataclasses import replace
from datetime import date, datetime
from ninja import UploadedFile
from api.src.domain.interface.media.video.data import VideoData
from api.src.domain.interface.media.music.data import MusicData
from api.src.domain.interface.media.comic.data import ComicData
from api.src.domain.interface.media.picture.data import PictureData
from api.src.domain.interface.media.blog.data import BlogData
from api.src.domain.interface.media.chat.data import ChatData
from api.src.domain.interface.media.video.interface import VideoInterface
from api.src.domain.interface.media.music.interface import MusicInterface
from api.src.domain.interface.media.comic.interface import ComicInterface
from api.src.domain.interface.media.picture.interface import PictureInterface
from api.src.domain.interface.media.blog.interface import BlogInterface
from api.src.domain.interface.media.chat.interface import ChatInterface
from api.src.domain.interface.channel.data import ChannelData
from api.src.domain.interface.media.index import FilterOption, SortOption, ExcludeOption
from api.src.injectors.container import injector
from api.src.types.data.media import MediaCreateData, HomeData, VideoDetailData, MusicDetailData, ComicDetailData, PictureDetailData, BlogDetailData, ChatDetailData
from api.src.types.schema.media import VideoIn, MusicIn, ComicIn, PictureIn, BlogIn, ChatIn
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
        like=0,
        publish=True,
        created=datetime.min,
        updated=datetime.min,
        comment_count=0,
        channel=channel,
        hashtags=[],
    )

    new_ids = repository.bulk_save([new_video])
    assert len(new_ids) == 1, "作成に失敗しました"
    obj = repository.bulk_get(new_ids)[0]

    return MediaCreateData(ulid=obj.ulid)


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
        like=0,
        download=input.download,
        publish=True,
        created=datetime.min,
        updated=datetime.min,
        comment_count=0,
        channel=channel,
        hashtags=[],
    )

    new_ids = repository.bulk_save([new_music])
    assert len(new_ids) == 1, "作成に失敗しました"
    obj = repository.bulk_get(new_ids)[0]

    return MediaCreateData(ulid=obj.ulid)


def create_comic(channel: ChannelData, input: ComicIn, image: UploadedFile) -> MediaCreateData:
    repository = injector.get(ComicInterface)

    new_comic = ComicData(
        id=0,
        ulid="",
        title=input.title,
        content=input.content,
        image=image.name or "",
        read=0,
        like=0,
        publish=True,
        created=datetime.min,
        updated=datetime.min,
        comment_count=0,
        channel=channel,
        hashtags=[],
    )

    new_ids = repository.bulk_save([new_comic])
    assert len(new_ids) == 1, "作成に失敗しました"
    obj = repository.bulk_get(new_ids)[0]

    return MediaCreateData(ulid=obj.ulid)


def create_picture(channel: ChannelData, input: PictureIn, image: UploadedFile) -> MediaCreateData:
    repository = injector.get(PictureInterface)

    new_picture = PictureData(
        id=0,
        ulid="",
        title=input.title,
        content=input.content,
        image=image.name or "",
        read=0,
        like=0,
        publish=True,
        created=datetime.min,
        updated=datetime.min,
        comment_count=0,
        channel=channel,
        hashtags=[],
    )

    new_ids = repository.bulk_save([new_picture])
    assert len(new_ids) == 1, "作成に失敗しました"
    obj = repository.bulk_get(new_ids)[0]

    return MediaCreateData(ulid=obj.ulid)


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
        like=0,
        publish=True,
        created=datetime.min,
        updated=datetime.min,
        comment_count=0,
        channel=channel,
        hashtags=[],
    )

    new_ids = repository.bulk_save([new_blog])
    assert len(new_ids) == 1, "作成に失敗しました"
    obj = repository.bulk_get(new_ids)[0]

    return MediaCreateData(ulid=obj.ulid)


def create_chat(channel: ChannelData, input: ChatIn) -> MediaCreateData:
    repository = injector.get(ChatInterface)

    new_chat = ChatData(
        id=0,
        ulid="",
        title=input.title,
        content=input.content,
        read=0,
        like=0,
        period=date.fromisoformat(input.period),
        publish=True,
        created=datetime.min,
        updated=datetime.min,
        thread_count=0,
        joined_count=0,
        channel=channel,
        hashtags=[],
    )

    new_ids = repository.bulk_save([new_chat])
    assert len(new_ids) == 1, "作成に失敗しました"
    obj = repository.bulk_get(new_ids)[0]

    return MediaCreateData(ulid=obj.ulid)


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
    repository = injector.get(VideoInterface)
    ids = repository.get_ids(FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)
    objs = repository.bulk_get(ids=ids)

    data = [replace(o,
        image=create_url(o.image),
        video=create_url(o.video),
        convert=create_url(o.convert),
    ) for o in objs]

    return data


def get_musics(limit: int, search: str, id: int | None = None) -> list[MusicData]:
    repository = injector.get(MusicInterface)
    ids = repository.get_ids(FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)
    objs = repository.bulk_get(ids=ids)
    data = [replace(o, music=create_url(o.music)) for o in objs]
    return data


def get_comics(limit: int, search: str, id: int | None = None) -> list[ComicData]:
    repository = injector.get(ComicInterface)
    ids = repository.get_ids(FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)
    objs = repository.bulk_get(ids=ids)
    data = [replace(o, image=create_url(o.image)) for o in objs]
    return data


def get_pictures(limit: int, search: str, id: int | None = None) -> list[PictureData]:
    repository = injector.get(PictureInterface)
    ids = repository.get_ids(FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)
    objs = repository.bulk_get(ids=ids)
    data = [replace(o, image=create_url(o.image)) for o in objs]
    return data


def get_blogs(limit: int, search: str, id: int | None = None) -> list[BlogData]:
    repository = injector.get(BlogInterface)
    ids = repository.get_ids(FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)
    objs = repository.bulk_get(ids=ids)
    data = [replace(o, image=create_url(o.image)) for o in objs]
    return data


def get_chats(limit: int, search: str, id: int | None = None) -> list[ChatData]:
    repository = injector.get(ChatInterface)
    ids = repository.get_ids(FilterOption(search=search), ExcludeOption(id=id), SortOption(), limit)
    objs = repository.bulk_get(ids=ids)
    return objs


def get_video_detail(user_id: int | None, ulid: str, publish: bool = True) -> VideoDetailData:
    repository = injector.get(VideoInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption())
    assert len(ids) == 1, "データが見つかりませんでした"
    objs = repository.bulk_get(ids=ids)
    obj = objs[0]

    type_no = comment_type_no_map(CommentType.VIDEO)
    comments = get_comments(type_no=type_no, object_id=obj.id, user_id=user_id)
    is_like = repository.is_liked(obj.id, user_id) if user_id is not None else False

    data = VideoDetailData(
        id=obj.id,
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        image=create_url(obj.image),
        video=create_url(obj.video),
        convert=create_url(obj.convert),
        comments=comments,
        hashtags=obj.hashtags,
        read=obj.read,
        like=obj.like,
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        channel=obj.channel,
        mediaUser=get_media_user(is_like, obj.channel.id, user_id),
    )

    return data


def get_music_detail(user_id: int | None, ulid: str, publish: bool = True) -> MusicDetailData:
    repository = injector.get(MusicInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption())
    assert len(ids) == 1, "データが見つかりませんでした"
    objs = repository.bulk_get(ids=ids)
    obj = objs[0]

    type_no = comment_type_no_map(CommentType.MUSIC)
    comments = get_comments(type_no=type_no, object_id=obj.id, user_id=user_id)
    is_like = repository.is_liked(obj.id, user_id) if user_id is not None else False

    data = MusicDetailData(
        id=obj.id,
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        lyric=obj.lyric,
        music=create_url(obj.music),
        download=obj.download,
        comments=comments,
        hashtags=obj.hashtags,
        read=obj.read,
        like=obj.like,
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        channel=obj.channel,
        mediaUser=get_media_user(is_like, obj.channel.id, user_id),
    )

    return data


def get_comic_detail(user_id: int | None, ulid: str, publish: bool = True) -> ComicDetailData:
    repository = injector.get(ComicInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption())
    assert len(ids) == 1, "データが見つかりませんでした"
    objs = repository.bulk_get(ids=ids)
    obj = objs[0]

    type_no = comment_type_no_map(CommentType.COMIC)
    comments = get_comments(type_no=type_no, object_id=obj.id, user_id=user_id)
    is_like = repository.is_liked(obj.id, user_id) if user_id is not None else False

    data = ComicDetailData(
        id=obj.id,
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        image=create_url(obj.image),
        comments=comments,
        hashtags=obj.hashtags,
        read=obj.read,
        like=obj.like,
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        channel=obj.channel,
        mediaUser=get_media_user(is_like, obj.channel.id, user_id),
    )

    return data


def get_blog_detail(user_id: int | None, ulid: str, publish: bool = True) -> BlogDetailData:
    repository = injector.get(BlogInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption())
    assert len(ids) == 1, "データが見つかりませんでした"
    objs = repository.bulk_get(ids=ids)
    obj = objs[0]

    type_no = comment_type_no_map(CommentType.BLOG)
    comments = get_comments(type_no=type_no, object_id=obj.id, user_id=user_id)
    is_like = repository.is_liked(obj.id, user_id) if user_id is not None else False

    data = BlogDetailData(
        id=obj.id,
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        richtext=obj.richtext,
        image=create_url(obj.image),
        comments=comments,
        hashtags=obj.hashtags,
        read=obj.read,
        like=obj.like,
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        channel=obj.channel,
        mediaUser=get_media_user(is_like, obj.channel.id, user_id),
    )

    return data


def get_picture_detail(user_id: int | None, ulid: str, publish: bool = True) -> PictureDetailData:
    repository = injector.get(PictureInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption())
    assert len(ids) == 1, "データが見つかりませんでした"
    objs = repository.bulk_get(ids=ids)
    obj = objs[0]

    type_no = comment_type_no_map(CommentType.PICTURE)
    comments = get_comments(type_no=type_no, object_id=obj.id, user_id=None)
    is_like = repository.is_liked(obj.id, user_id) if user_id is not None else False

    data = PictureDetailData(
        id=obj.id,
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        image=create_url(obj.image),
        comments=comments,
        hashtags=obj.hashtags,
        read=obj.read,
        like=obj.like,
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        channel=obj.channel,
        mediaUser=get_media_user(is_like, obj.channel.id, user_id),
    )

    return data


def get_chat_detail(user_id: int | None, ulid: str, publish: bool = True) -> ChatDetailData:
    repository = injector.get(ChatInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption())
    assert len(ids) == 1, "データが見つかりませんでした"
    objs = repository.bulk_get(ids=ids)
    obj = objs[0]

    messages = get_messages(chat_id=obj.id)
    is_like = repository.is_liked(obj.id, user_id) if user_id is not None else False

    data = ChatDetailData(
        id=obj.id,
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        messages=messages,
        hashtags=obj.hashtags,
        read=obj.read,
        like=obj.like,
        thread=obj.thread_count,
        joined=obj.joined_count,
        period=obj.period,
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        channel=obj.channel,
        mediaUser=get_media_user(is_like, obj.channel.id, user_id),
    )

    return data
