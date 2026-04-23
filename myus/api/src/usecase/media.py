from dataclasses import replace
from datetime import date, datetime
from ninja import UploadedFile
from api.modules.logger import log
from api.src.domain.interface.media.video.data import VideoData
from api.src.domain.interface.media.music.data import MusicData
from api.src.domain.interface.media.blog.data import BlogData
from api.src.domain.interface.media.comic.data import ComicData
from api.src.domain.interface.media.picture.data import PictureData
from api.src.domain.interface.media.chat.data import ChatData
from api.src.domain.interface.media.video.interface import VideoInterface
from api.src.domain.interface.media.music.interface import MusicInterface
from api.src.domain.interface.media.blog.interface import BlogInterface
from api.src.domain.interface.media.comic.interface import ComicInterface
from api.src.domain.interface.media.picture.interface import PictureInterface
from api.src.domain.interface.media.chat.interface import ChatInterface
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, PageOption, SortOption, SortType
from api.src.injectors.container import injector
from api.src.types.dto.media import MediaCreateDTO, HomeDTO, VideoDetailDTO, MusicDetailDTO, BlogDetailDTO, ComicDetailDTO, PictureDetailDTO, ChatDetailDTO
from api.src.types.schema.media.input import VideoIn, MusicIn, BlogIn, ComicIn, PictureIn, ChatIn
from api.src.usecase.channel import get_channel_data
from api.src.usecase.comment import get_comments
from api.src.usecase.message import get_messages
from api.utils.enum.index import CommentType, ImageUpload, MediaUpload
from api.utils.functions.index import create_url
from api.utils.functions.map import comment_type_no_map
from api.utils.functions.user import get_media_user
from api.utils.functions.convert.encode_worker import EncodeWorker
from api.utils.functions.convert.video_encoding import convert_video
from api.utils.functions.media import save_upload


def create_video(input: VideoIn, image: UploadedFile, video: UploadedFile) -> MediaCreateDTO | None:
    channel = get_channel_data(input.channel_ulid)
    if channel is None:
        return None

    repository = injector.get(VideoInterface)
    video_path = save_upload(video, MediaUpload.VIDEO, channel.ulid)

    new_video = VideoData(
        id=0,
        ulid="",
        title=input.title,
        content=input.content,
        image=save_upload(image, ImageUpload.VIDEO, channel.ulid),
        video=video_path,
        convert="",
        read=0,
        like=0,
        publish=False,
        created=datetime.min,
        updated=datetime.min,
        channel=channel,
        hashtags=[],
    )

    new_ids = repository.bulk_save([new_video])
    assert len(new_ids) == 1, "作成に失敗しました"
    obj = repository.bulk_get(new_ids)[0]

    def encode_task() -> None:
        result = convert_video(video_path)
        videos = repository.bulk_get([obj.id])
        if len(videos) == 0:
            log.warning("動画が見つかりません", video_id=obj.id)
            return
        updated = replace(videos[0], video=result.video, convert=result.convert, publish=input.publish)
        repository.bulk_save([updated])

    EncodeWorker.submit(encode_task)

    return MediaCreateDTO(ulid=obj.ulid)


def create_music(input: MusicIn, music: UploadedFile) -> MediaCreateDTO | None:
    channel = get_channel_data(input.channel_ulid)
    if channel is None:
        return None

    repository = injector.get(MusicInterface)

    new_music = MusicData(
        id=0,
        ulid="",
        title=input.title,
        content=input.content,
        lyric=input.lyric,
        music=save_upload(music, MediaUpload.MUSIC, channel.ulid),
        read=0,
        like=0,
        download=input.download,
        publish=input.publish,
        created=datetime.min,
        updated=datetime.min,
        channel=channel,
        hashtags=[],
    )

    new_ids = repository.bulk_save([new_music])
    assert len(new_ids) == 1, "作成に失敗しました"
    obj = repository.bulk_get(new_ids)[0]

    return MediaCreateDTO(ulid=obj.ulid)


def create_blog(input: BlogIn, image: UploadedFile) -> MediaCreateDTO | None:
    channel = get_channel_data(input.channel_ulid)
    if channel is None:
        return None

    repository = injector.get(BlogInterface)

    new_blog = BlogData(
        id=0,
        ulid="",
        title=input.title,
        content=input.content,
        richtext=input.richtext,
        delta="",
        image=save_upload(image, ImageUpload.BLOG, channel.ulid),
        read=0,
        like=0,
        publish=input.publish,
        created=datetime.min,
        updated=datetime.min,
        channel=channel,
        hashtags=[],
    )

    new_ids = repository.bulk_save([new_blog])
    assert len(new_ids) == 1, "作成に失敗しました"
    obj = repository.bulk_get(new_ids)[0]

    return MediaCreateDTO(ulid=obj.ulid)


def create_comic(input: ComicIn, image: UploadedFile, pages: list[UploadedFile]) -> MediaCreateDTO | None:
    channel = get_channel_data(input.channel_ulid)
    if channel is None:
        return None

    repository = injector.get(ComicInterface)

    new_comic = ComicData(
        id=0,
        ulid="",
        title=input.title,
        content=input.content,
        image=save_upload(image, ImageUpload.COMIC, channel.ulid),
        pages=[save_upload(p, ImageUpload.COMIC_PAGE, channel.ulid) for p in pages],
        read=0,
        like=0,
        publish=input.publish,
        created=datetime.min,
        updated=datetime.min,
        channel=channel,
        hashtags=[],
    )

    new_ids = repository.bulk_save([new_comic])
    assert len(new_ids) == 1, "作成に失敗しました"
    obj = repository.bulk_get(new_ids)[0]

    return MediaCreateDTO(ulid=obj.ulid)


def create_picture(input: PictureIn, image: UploadedFile) -> MediaCreateDTO | None:
    channel = get_channel_data(input.channel_ulid)
    if channel is None:
        return None

    repository = injector.get(PictureInterface)

    new_picture = PictureData(
        id=0,
        ulid="",
        title=input.title,
        content=input.content,
        image=save_upload(image, ImageUpload.PICTURE, channel.ulid),
        read=0,
        like=0,
        publish=input.publish,
        created=datetime.min,
        updated=datetime.min,
        channel=channel,
        hashtags=[],
    )

    new_ids = repository.bulk_save([new_picture])
    assert len(new_ids) == 1, "作成に失敗しました"
    obj = repository.bulk_get(new_ids)[0]

    return MediaCreateDTO(ulid=obj.ulid)


def create_chat(input: ChatIn) -> MediaCreateDTO | None:
    channel = get_channel_data(input.channel_ulid)
    if channel is None:
        return None

    repository = injector.get(ChatInterface)

    new_chat = ChatData(
        id=0,
        ulid="",
        title=input.title,
        content=input.content,
        read=0,
        like=0,
        period=date.fromisoformat(input.period),
        publish=input.publish,
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

    return MediaCreateDTO(ulid=obj.ulid)


def get_home(limit: int, search: str) -> HomeDTO:
    videos, _ = get_videos(limit, 0, search)
    musics, _ = get_musics(limit, 0, search)
    blogs, _ = get_blogs(limit, 0, search)
    comics, _ = get_comics(limit, 0, search)
    pictures, _ = get_pictures(limit, 0, search)
    chats, _ = get_chats(limit, 0, search)
    return HomeDTO(videos=videos, musics=musics, blogs=blogs, comics=comics, pictures=pictures, chats=chats)


def get_recommend(limit: int, search: str) -> HomeDTO:
    videos, _ = get_videos(limit, 0, search, is_recommend=True)
    musics, _ = get_musics(limit, 0, search, is_recommend=True)
    blogs, _ = get_blogs(limit, 0, search, is_recommend=True)
    comics, _ = get_comics(limit, 0, search, is_recommend=True)
    pictures, _ = get_pictures(limit, 0, search, is_recommend=True)
    chats, _ = get_chats(limit, 0, search, is_recommend=True)
    return HomeDTO(videos=videos, musics=musics, blogs=blogs, comics=comics, pictures=pictures, chats=chats)


def get_videos(limit: int, offset: int, search: str, id: int = 0, channel_id: int = 0, is_recommend: bool = False, user_id: int | None = None) -> tuple[list[VideoData], int]:
    repository = injector.get(VideoInterface)
    filter = FilterOption(search=search, publish=True, channel_id=channel_id, is_recommend=is_recommend)
    sort = SortOption(sort_type=SortType.SCORE)
    total = repository.count(filter)
    ids = repository.get_ids(filter, ExcludeOption(id=id), sort, PageOption(limit=limit, offset=offset), user_id)
    objs = repository.bulk_get(ids=ids)

    data = [replace(o,
        image=create_url(o.image),
        video=create_url(o.video),
        convert=create_url(o.convert),
    ) for o in objs]

    return data, total


def get_musics(limit: int, offset: int, search: str, id: int = 0, channel_id: int = 0, is_recommend: bool = False, user_id: int | None = None) -> tuple[list[MusicData], int]:
    repository = injector.get(MusicInterface)
    filter = FilterOption(search=search, publish=True, channel_id=channel_id, is_recommend=is_recommend)
    sort = SortOption(sort_type=SortType.SCORE)
    total = repository.count(filter)
    ids = repository.get_ids(filter, ExcludeOption(id=id), sort, PageOption(limit=limit, offset=offset), user_id)
    objs = repository.bulk_get(ids=ids)
    data = [replace(o, music=create_url(o.music)) for o in objs]
    return data, total


def get_blogs(limit: int, offset: int, search: str, id: int = 0, channel_id: int = 0, is_recommend: bool = False, user_id: int | None = None) -> tuple[list[BlogData], int]:
    repository = injector.get(BlogInterface)
    filter = FilterOption(search=search, publish=True, channel_id=channel_id, is_recommend=is_recommend)
    sort = SortOption(sort_type=SortType.SCORE)
    total = repository.count(filter)
    ids = repository.get_ids(filter, ExcludeOption(id=id), sort, PageOption(limit=limit, offset=offset), user_id)
    objs = repository.bulk_get(ids=ids)
    data = [replace(o, image=create_url(o.image)) for o in objs]
    return data, total


def get_comics(limit: int, offset: int, search: str, id: int = 0, channel_id: int = 0, is_recommend: bool = False, user_id: int | None = None) -> tuple[list[ComicData], int]:
    repository = injector.get(ComicInterface)
    filter = FilterOption(search=search, publish=True, channel_id=channel_id, is_recommend=is_recommend)
    sort = SortOption(sort_type=SortType.SCORE)
    total = repository.count(filter)
    ids = repository.get_ids(filter, ExcludeOption(id=id), sort, PageOption(limit=limit, offset=offset), user_id)
    objs = repository.bulk_get(ids=ids)

    data = [replace(o,
        image=create_url(o.image),
        pages=[create_url(p) for p in o.pages],
    ) for o in objs]

    return data, total


def get_pictures(limit: int, offset: int, search: str, id: int = 0, channel_id: int = 0, is_recommend: bool = False, user_id: int | None = None) -> tuple[list[PictureData], int]:
    repository = injector.get(PictureInterface)
    filter = FilterOption(search=search, publish=True, channel_id=channel_id, is_recommend=is_recommend)
    sort = SortOption(sort_type=SortType.SCORE)
    total = repository.count(filter)
    ids = repository.get_ids(filter, ExcludeOption(id=id), sort, PageOption(limit=limit, offset=offset), user_id)
    objs = repository.bulk_get(ids=ids)
    data = [replace(o, image=create_url(o.image)) for o in objs]
    return data, total


def get_chats(limit: int, offset: int, search: str, id: int = 0, channel_id: int = 0, is_recommend: bool = False, user_id: int | None = None) -> tuple[list[ChatData], int]:
    repository = injector.get(ChatInterface)
    filter = FilterOption(search=search, publish=True, channel_id=channel_id, is_recommend=is_recommend)
    sort = SortOption(sort_type=SortType.SCORE)
    total = repository.count(filter)
    ids = repository.get_ids(filter, ExcludeOption(id=id), sort, PageOption(limit=limit, offset=offset), user_id)
    objs = repository.bulk_get(ids=ids)
    return objs, total


def get_video_detail(user_id: int | None, ulid: str, publish: bool = True) -> VideoDetailDTO:
    repository = injector.get(VideoInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption(), PageOption(limit=1))
    assert len(ids) == 1, "データが見つかりませんでした"
    objs = repository.bulk_get(ids=ids)
    obj = objs[0]

    type_no = comment_type_no_map(CommentType.VIDEO)
    comments = get_comments(type_no=type_no, object_id=obj.id, user_id=user_id)
    is_like = repository.is_liked(obj.id, user_id) if user_id is not None else False

    data = VideoDetailDTO(
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


def get_music_detail(user_id: int | None, ulid: str, publish: bool = True) -> MusicDetailDTO:
    repository = injector.get(MusicInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption(), PageOption(limit=1))
    assert len(ids) == 1, "データが見つかりませんでした"
    objs = repository.bulk_get(ids=ids)
    obj = objs[0]

    type_no = comment_type_no_map(CommentType.MUSIC)
    comments = get_comments(type_no=type_no, object_id=obj.id, user_id=user_id)
    is_like = repository.is_liked(obj.id, user_id) if user_id is not None else False

    data = MusicDetailDTO(
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


def get_blog_detail(user_id: int | None, ulid: str, publish: bool = True) -> BlogDetailDTO:
    repository = injector.get(BlogInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption(), PageOption(limit=1))
    assert len(ids) == 1, "データが見つかりませんでした"
    objs = repository.bulk_get(ids=ids)
    obj = objs[0]

    type_no = comment_type_no_map(CommentType.BLOG)
    comments = get_comments(type_no=type_no, object_id=obj.id, user_id=user_id)
    is_like = repository.is_liked(obj.id, user_id) if user_id is not None else False

    data = BlogDetailDTO(
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


def get_comic_detail(user_id: int | None, ulid: str, publish: bool = True) -> ComicDetailDTO:
    repository = injector.get(ComicInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption(), PageOption(limit=1))
    assert len(ids) == 1, "データが見つかりませんでした"
    objs = repository.bulk_get(ids=ids)
    obj = objs[0]

    type_no = comment_type_no_map(CommentType.COMIC)
    comments = get_comments(type_no=type_no, object_id=obj.id, user_id=user_id)
    is_like = repository.is_liked(obj.id, user_id) if user_id is not None else False

    data = ComicDetailDTO(
        id=obj.id,
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        image=create_url(obj.image),
        pages=[create_url(p) for p in obj.pages],
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


def get_picture_detail(user_id: int | None, ulid: str, publish: bool = True) -> PictureDetailDTO:
    repository = injector.get(PictureInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption(), PageOption(limit=1))
    assert len(ids) == 1, "データが見つかりませんでした"
    objs = repository.bulk_get(ids=ids)
    obj = objs[0]

    type_no = comment_type_no_map(CommentType.PICTURE)
    comments = get_comments(type_no=type_no, object_id=obj.id, user_id=None)
    is_like = repository.is_liked(obj.id, user_id) if user_id is not None else False

    data = PictureDetailDTO(
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


def get_chat_detail(user_id: int | None, ulid: str, publish: bool = True) -> ChatDetailDTO:
    repository = injector.get(ChatInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption(), PageOption(limit=1))
    assert len(ids) == 1, "データが見つかりませんでした"
    objs = repository.bulk_get(ids=ids)
    obj = objs[0]

    messages = get_messages(chat_id=obj.id)
    is_like = repository.is_liked(obj.id, user_id) if user_id is not None else False

    data = ChatDetailDTO(
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
