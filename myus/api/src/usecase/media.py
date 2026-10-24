from dataclasses import replace
from datetime import date, datetime
from django.db import transaction
from ninja import UploadedFile
from api.modules.logger import log
from api.src.domain.interface.category.interface import CategoryInterface
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
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, PAGE_SIZE, PageOption, SortOption, SortType
from api.src.domain.interface.notification.interface import NotificationInterface
from api.src.injectors.container import injector
from api.src.types.dto.media import MediaCreateDTO, HomeDTO, VideoDetailDTO, MusicDetailDTO, BlogDetailDTO, ComicDetailDTO, PictureDetailDTO, ChatDetailDTO
from api.src.types.schema.media.input import VideoIn, MusicIn, BlogIn, ComicIn, PictureIn, ChatIn
from api.src.usecase.access_log import record_access
from api.src.usecase.category import get_category_data
from api.src.usecase.channel import get_channel_data
from api.src.usecase.comment import get_comments
from api.src.usecase.message import get_messages
from api.src.usecase.notification import create_notification
from api.src.usecase.user import get_user_data
from api.utils.common.result import AccessError, FatalError, FindError, ForbiddenError, NotFoundError, Result, ValidationError, WriteError
from api.utils.enum.access_log import AccessType
from api.utils.enum.media import CommentType, MediaType
from api.utils.enum.notification import NotificationObjectType, NotificationTypeNo
from api.utils.enum.upload import ImageUpload, MediaUpload
from api.utils.functions.index import create_url
from api.utils.functions.map import comment_type_no_map
from api.utils.functions.user import get_media_user
from api.utils.functions.convert.encode_worker import EncodeWorker
from api.utils.functions.convert.video_encoding import convert_video
from api.utils.functions.media import get_media_repository, save_upload, validate_uploads
from api.utils.plan import get_plan


VIEWS_THRESHOLDS = (10000, 100000, 1000000, 10000000, 100000000, 1000000000)


@Result.shield_exception()
def create_video(user_id: int, input: VideoIn, image: UploadedFile, video: UploadedFile) -> Result[MediaCreateDTO, WriteError]:
    upload_ret = validate_uploads([(video, MediaUpload.VIDEO), (image, ImageUpload.VIDEO)])
    if upload_ret.is_err:
        return Result.err(upload_ret.err_value)

    channel_ret = get_channel_data(input.channel_ulid)
    if channel_ret.is_err:
        return Result.err(channel_ret.err_value)

    channel = channel_ret.ok_value
    if channel is None:
        return Result.err(NotFoundError("error.channelNotFound"))

    if channel.owner_id != user_id:
        log.warning("チャンネルの持ち主ではありません", channel_ulid=channel.ulid, user_id=user_id)
        return Result.err(ForbiddenError("Forbidden"))

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
        category_ulid="",
        hashtags=[],
    )

    repo = injector.get(VideoInterface)
    category_repo = injector.get(CategoryInterface)
    category_data_ret = get_category_data(input.category_ulid)
    if category_data_ret.is_err:
        return Result.err(category_data_ret.err_value)

    category_data = category_data_ret.ok_value
    if category_data is None:
        return Result.err(ValidationError("error.categoryRequired"))

    with transaction.atomic():
        ids_ret = repo.bulk_save([new_video])
        if ids_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(ids_ret.err_value)

        new_ids = ids_ret.ok_value
        assert len(new_ids) == 1, "作成に失敗しました"
        category_ret = category_repo.bulk_save(MediaType.VIDEO, new_ids[0], [category_data])
        if category_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(category_ret.err_value)

    objs_ret = repo.bulk_get(new_ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]

    def encode_task() -> None:
        result = convert_video(video_path)
        if result.video == "":
            log.error("動画のエンコードに失敗しました", video_id=obj.id)
            return

        videos_ret = repo.bulk_get([obj.id])
        if videos_ret.is_err:
            log.error("動画の取得に失敗しました", error=videos_ret.err_value.message, video_id=obj.id)
            return

        videos = videos_ret.ok_value
        if len(videos) == 0:
            log.warning("動画が見つかりません", video_id=obj.id)
            return
        video = videos[0]
        publish = input.publish if video.updated == obj.updated else video.publish
        updated = replace(video, video=result.video, convert=result.convert, publish=publish)
        save_ret = repo.bulk_save([updated])
        if save_ret.is_err:
            log.error("動画の保存に失敗しました", error=save_ret.err_value.message, video_id=obj.id)
            return

        if publish:
            notification_ret = create_notification(channel.owner_id, 0, NotificationTypeNo.VIDEO, obj.id, NotificationObjectType.VIDEO)
            if notification_ret.is_err:
                log.error("通知の作成に失敗しました", error=notification_ret.err_value.message, video_id=obj.id)

    EncodeWorker.submit(encode_task)

    return Result.ok(MediaCreateDTO(ulid=obj.ulid))


@Result.shield_exception()
def create_music(user_id: int, input: MusicIn, music: UploadedFile) -> Result[MediaCreateDTO, WriteError]:
    upload_ret = validate_uploads([(music, MediaUpload.MUSIC)])
    if upload_ret.is_err:
        return Result.err(upload_ret.err_value)

    channel_ret = get_channel_data(input.channel_ulid)
    if channel_ret.is_err:
        return Result.err(channel_ret.err_value)

    channel = channel_ret.ok_value
    if channel is None:
        return Result.err(NotFoundError("error.channelNotFound"))

    if channel.owner_id != user_id:
        log.warning("チャンネルの持ち主ではありません", channel_ulid=channel.ulid, user_id=user_id)
        return Result.err(ForbiddenError("Forbidden"))

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
        category_ulid="",
        hashtags=[],
    )

    repo = injector.get(MusicInterface)
    category_repo = injector.get(CategoryInterface)
    category_data_ret = get_category_data(input.category_ulid)
    if category_data_ret.is_err:
        return Result.err(category_data_ret.err_value)

    category_data = category_data_ret.ok_value
    if category_data is None:
        return Result.err(ValidationError("error.categoryRequired"))

    with transaction.atomic():
        ids_ret = repo.bulk_save([new_music])
        if ids_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(ids_ret.err_value)

        new_ids = ids_ret.ok_value
        assert len(new_ids) == 1, "作成に失敗しました"
        category_ret = category_repo.bulk_save(MediaType.MUSIC, new_ids[0], [category_data])
        if category_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(category_ret.err_value)

    objs_ret = repo.bulk_get(new_ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]
    if input.publish:
        notification_ret = create_notification(channel.owner_id, 0, NotificationTypeNo.MUSIC, obj.id, NotificationObjectType.MUSIC)
        if notification_ret.is_err:
            log.error("通知の作成に失敗しました", error=notification_ret.err_value.message, music_id=obj.id)

    return Result.ok(MediaCreateDTO(ulid=obj.ulid))


@Result.shield_exception()
def create_blog(user_id: int, input: BlogIn, image: UploadedFile) -> Result[MediaCreateDTO, WriteError]:
    upload_ret = validate_uploads([(image, ImageUpload.BLOG)])
    if upload_ret.is_err:
        return Result.err(upload_ret.err_value)

    channel_ret = get_channel_data(input.channel_ulid)
    if channel_ret.is_err:
        return Result.err(channel_ret.err_value)

    channel = channel_ret.ok_value
    if channel is None:
        return Result.err(NotFoundError("error.channelNotFound"))

    if channel.owner_id != user_id:
        log.warning("チャンネルの持ち主ではありません", channel_ulid=channel.ulid, user_id=user_id)
        return Result.err(ForbiddenError("Forbidden"))

    new_blog = BlogData(
        id=0,
        ulid="",
        title=input.title,
        content=input.content,
        richtext=input.richtext,
        is_promotion=input.is_promotion,
        image=save_upload(image, ImageUpload.BLOG, channel.ulid),
        read=0,
        like=0,
        publish=input.publish,
        created=datetime.min,
        updated=datetime.min,
        channel=channel,
        category_ulid="",
        hashtags=[],
    )

    repo = injector.get(BlogInterface)
    category_repo = injector.get(CategoryInterface)
    category_data_ret = get_category_data(input.category_ulid)
    if category_data_ret.is_err:
        return Result.err(category_data_ret.err_value)

    category_data = category_data_ret.ok_value
    if category_data is None:
        return Result.err(ValidationError("error.categoryRequired"))

    with transaction.atomic():
        ids_ret = repo.bulk_save([new_blog])
        if ids_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(ids_ret.err_value)

        new_ids = ids_ret.ok_value
        assert len(new_ids) == 1, "作成に失敗しました"
        category_ret = category_repo.bulk_save(MediaType.BLOG, new_ids[0], [category_data])
        if category_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(category_ret.err_value)

    objs_ret = repo.bulk_get(new_ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]
    if input.publish:
        notification_ret = create_notification(channel.owner_id, 0, NotificationTypeNo.BLOG, obj.id, NotificationObjectType.BLOG)
        if notification_ret.is_err:
            log.error("通知の作成に失敗しました", error=notification_ret.err_value.message, blog_id=obj.id)

    return Result.ok(MediaCreateDTO(ulid=obj.ulid))


@Result.shield_exception()
def create_comic(user_id: int, input: ComicIn, image: UploadedFile, pages: list[UploadedFile]) -> Result[MediaCreateDTO, WriteError]:
    upload_ret = validate_uploads([(image, ImageUpload.COMIC), *[(p, ImageUpload.COMIC_PAGE) for p in pages]])
    if upload_ret.is_err:
        return Result.err(upload_ret.err_value)

    channel_ret = get_channel_data(input.channel_ulid)
    if channel_ret.is_err:
        return Result.err(channel_ret.err_value)

    channel = channel_ret.ok_value
    if channel is None:
        return Result.err(NotFoundError("error.channelNotFound"))

    if channel.owner_id != user_id:
        log.warning("チャンネルの持ち主ではありません", channel_ulid=channel.ulid, user_id=user_id)
        return Result.err(ForbiddenError("Forbidden"))

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
        category_ulid="",
        hashtags=[],
    )

    repo = injector.get(ComicInterface)
    category_repo = injector.get(CategoryInterface)
    category_data_ret = get_category_data(input.category_ulid)
    if category_data_ret.is_err:
        return Result.err(category_data_ret.err_value)

    category_data = category_data_ret.ok_value
    if category_data is None:
        return Result.err(ValidationError("error.categoryRequired"))

    with transaction.atomic():
        ids_ret = repo.bulk_save([new_comic])
        if ids_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(ids_ret.err_value)

        new_ids = ids_ret.ok_value
        assert len(new_ids) == 1, "作成に失敗しました"
        category_ret = category_repo.bulk_save(MediaType.COMIC, new_ids[0], [category_data])
        if category_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(category_ret.err_value)

    objs_ret = repo.bulk_get(new_ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]
    if input.publish:
        notification_ret = create_notification(channel.owner_id, 0, NotificationTypeNo.COMIC, obj.id, NotificationObjectType.COMIC)
        if notification_ret.is_err:
            log.error("通知の作成に失敗しました", error=notification_ret.err_value.message, comic_id=obj.id)

    return Result.ok(MediaCreateDTO(ulid=obj.ulid))


@Result.shield_exception()
def create_picture(user_id: int, input: PictureIn, image: UploadedFile) -> Result[MediaCreateDTO, WriteError]:
    upload_ret = validate_uploads([(image, ImageUpload.PICTURE)])
    if upload_ret.is_err:
        return Result.err(upload_ret.err_value)

    channel_ret = get_channel_data(input.channel_ulid)
    if channel_ret.is_err:
        return Result.err(channel_ret.err_value)

    channel = channel_ret.ok_value
    if channel is None:
        return Result.err(NotFoundError("error.channelNotFound"))

    if channel.owner_id != user_id:
        log.warning("チャンネルの持ち主ではありません", channel_ulid=channel.ulid, user_id=user_id)
        return Result.err(ForbiddenError("Forbidden"))

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
        category_ulid="",
        hashtags=[],
    )

    repo = injector.get(PictureInterface)
    category_repo = injector.get(CategoryInterface)
    category_data_ret = get_category_data(input.category_ulid)
    if category_data_ret.is_err:
        return Result.err(category_data_ret.err_value)

    category_data = category_data_ret.ok_value
    if category_data is None:
        return Result.err(ValidationError("error.categoryRequired"))

    with transaction.atomic():
        ids_ret = repo.bulk_save([new_picture])
        if ids_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(ids_ret.err_value)

        new_ids = ids_ret.ok_value
        assert len(new_ids) == 1, "作成に失敗しました"
        category_ret = category_repo.bulk_save(MediaType.PICTURE, new_ids[0], [category_data])
        if category_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(category_ret.err_value)

    objs_ret = repo.bulk_get(new_ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]
    if input.publish:
        notification_ret = create_notification(channel.owner_id, 0, NotificationTypeNo.PICTURE, obj.id, NotificationObjectType.PICTURE)
        if notification_ret.is_err:
            log.error("通知の作成に失敗しました", error=notification_ret.err_value.message, picture_id=obj.id)

    return Result.ok(MediaCreateDTO(ulid=obj.ulid))


@Result.shield_exception()
def create_chat(user_id: int, input: ChatIn) -> Result[MediaCreateDTO, WriteError]:
    channel_ret = get_channel_data(input.channel_ulid)
    if channel_ret.is_err:
        return Result.err(channel_ret.err_value)

    channel = channel_ret.ok_value
    if channel is None:
        return Result.err(NotFoundError("error.channelNotFound"))

    if channel.owner_id != user_id:
        log.warning("チャンネルの持ち主ではありません", channel_ulid=channel.ulid, user_id=user_id)
        return Result.err(ForbiddenError("Forbidden"))

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
        category_ulid="",
        hashtags=[],
    )

    repo = injector.get(ChatInterface)
    category_repo = injector.get(CategoryInterface)
    category_data_ret = get_category_data(input.category_ulid)
    if category_data_ret.is_err:
        return Result.err(category_data_ret.err_value)

    category_data = category_data_ret.ok_value
    if category_data is None:
        return Result.err(ValidationError("error.categoryRequired"))

    with transaction.atomic():
        ids_ret = repo.bulk_save([new_chat])
        if ids_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(ids_ret.err_value)

        new_ids = ids_ret.ok_value
        assert len(new_ids) == 1, "作成に失敗しました"
        category_ret = category_repo.bulk_save(MediaType.CHAT, new_ids[0], [category_data])
        if category_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(category_ret.err_value)

    objs_ret = repo.bulk_get(new_ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]
    if input.publish:
        notification_ret = create_notification(channel.owner_id, 0, NotificationTypeNo.CHAT, obj.id, NotificationObjectType.CHAT)
        if notification_ret.is_err:
            log.error("通知の作成に失敗しました", error=notification_ret.err_value.message, chat_id=obj.id)

    return Result.ok(MediaCreateDTO(ulid=obj.ulid))


@Result.shield_exception()
def get_home(limit: int, search: str) -> Result[HomeDTO, FatalError]:
    videos_ret = get_videos(search, limit=limit)
    if videos_ret.is_err:
        return Result.err(videos_ret.err_value)

    musics_ret = get_musics(search, limit=limit)
    if musics_ret.is_err:
        return Result.err(musics_ret.err_value)

    blogs_ret = get_blogs(search, limit=limit)
    if blogs_ret.is_err:
        return Result.err(blogs_ret.err_value)

    comics_ret = get_comics(search, limit=limit)
    if comics_ret.is_err:
        return Result.err(comics_ret.err_value)

    pictures_ret = get_pictures(search, limit=limit)
    if pictures_ret.is_err:
        return Result.err(pictures_ret.err_value)

    chats_ret = get_chats(search, limit=limit)
    if chats_ret.is_err:
        return Result.err(chats_ret.err_value)

    videos, _ = videos_ret.ok_value
    musics, _ = musics_ret.ok_value
    blogs, _ = blogs_ret.ok_value
    comics, _ = comics_ret.ok_value
    pictures, _ = pictures_ret.ok_value
    chats, _ = chats_ret.ok_value
    return Result.ok(HomeDTO(videos=videos, musics=musics, blogs=blogs, comics=comics, pictures=pictures, chats=chats))


@Result.shield_exception()
def get_recommend(limit: int, search: str) -> Result[HomeDTO, FatalError]:
    videos_ret = get_videos(search, is_recommend=True, limit=limit)
    if videos_ret.is_err:
        return Result.err(videos_ret.err_value)

    musics_ret = get_musics(search, is_recommend=True, limit=limit)
    if musics_ret.is_err:
        return Result.err(musics_ret.err_value)

    blogs_ret = get_blogs(search, is_recommend=True, limit=limit)
    if blogs_ret.is_err:
        return Result.err(blogs_ret.err_value)

    comics_ret = get_comics(search, is_recommend=True, limit=limit)
    if comics_ret.is_err:
        return Result.err(comics_ret.err_value)

    pictures_ret = get_pictures(search, is_recommend=True, limit=limit)
    if pictures_ret.is_err:
        return Result.err(pictures_ret.err_value)

    chats_ret = get_chats(search, is_recommend=True, limit=limit)
    if chats_ret.is_err:
        return Result.err(chats_ret.err_value)

    videos, _ = videos_ret.ok_value
    musics, _ = musics_ret.ok_value
    blogs, _ = blogs_ret.ok_value
    comics, _ = comics_ret.ok_value
    pictures, _ = pictures_ret.ok_value
    chats, _ = chats_ret.ok_value
    return Result.ok(HomeDTO(videos=videos, musics=musics, blogs=blogs, comics=comics, pictures=pictures, chats=chats))


@Result.shield_exception()
def get_videos(search: str, id: int = 0, channel_id: int = 0, owner_id: int = 0, user_id: int | None = None, is_recommend: bool = False, limit: int = PAGE_SIZE, offset: int = 0) -> Result[tuple[list[VideoData], int], FatalError]:
    repo = injector.get(VideoInterface)
    filter = FilterOption(search=search, publish=True, owner_id=owner_id, channel_id=channel_id, is_recommend=is_recommend)
    sort = SortOption(sort_type=SortType.SCORE)
    count_ret = repo.count(filter)
    if count_ret.is_err:
        return Result.err(count_ret.err_value)

    total = count_ret.ok_value
    ids_ret = repo.get_ids(filter, ExcludeOption(id=id), sort, PageOption(limit=limit, offset=offset), user_id)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    objs_ret = repo.bulk_get(ids=ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value

    data = [replace(o,
        image=create_url(o.image),
        video=create_url(o.video),
        convert=create_url(o.convert),
    ) for o in objs]

    return Result.ok((data, total))


@Result.shield_exception()
def get_musics(search: str, id: int = 0, channel_id: int = 0, owner_id: int = 0, user_id: int | None = None, is_recommend: bool = False, limit: int = PAGE_SIZE, offset: int = 0) -> Result[tuple[list[MusicData], int], FatalError]:
    repo = injector.get(MusicInterface)
    filter = FilterOption(search=search, publish=True, owner_id=owner_id, channel_id=channel_id, is_recommend=is_recommend)
    sort = SortOption(sort_type=SortType.SCORE)
    count_ret = repo.count(filter)
    if count_ret.is_err:
        return Result.err(count_ret.err_value)

    total = count_ret.ok_value
    ids_ret = repo.get_ids(filter, ExcludeOption(id=id), sort, PageOption(limit=limit, offset=offset), user_id)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    objs_ret = repo.bulk_get(ids=ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    data = [replace(o, music=create_url(o.music)) for o in objs]
    return Result.ok((data, total))


@Result.shield_exception()
def get_blogs(search: str, id: int = 0, channel_id: int = 0, owner_id: int = 0, user_id: int | None = None, is_recommend: bool = False, limit: int = PAGE_SIZE, offset: int = 0) -> Result[tuple[list[BlogData], int], FatalError]:
    repo = injector.get(BlogInterface)
    filter = FilterOption(search=search, publish=True, owner_id=owner_id, channel_id=channel_id, is_recommend=is_recommend)
    sort = SortOption(sort_type=SortType.SCORE)
    count_ret = repo.count(filter)
    if count_ret.is_err:
        return Result.err(count_ret.err_value)

    total = count_ret.ok_value
    ids_ret = repo.get_ids(filter, ExcludeOption(id=id), sort, PageOption(limit=limit, offset=offset), user_id)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    objs_ret = repo.bulk_get(ids=ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    data = [replace(o, image=create_url(o.image)) for o in objs]
    return Result.ok((data, total))


@Result.shield_exception()
def get_comics(search: str, id: int = 0, channel_id: int = 0, owner_id: int = 0, user_id: int | None = None, is_recommend: bool = False, limit: int = PAGE_SIZE, offset: int = 0) -> Result[tuple[list[ComicData], int], FatalError]:
    repo = injector.get(ComicInterface)
    filter = FilterOption(search=search, publish=True, owner_id=owner_id, channel_id=channel_id, is_recommend=is_recommend)
    sort = SortOption(sort_type=SortType.SCORE)
    count_ret = repo.count(filter)
    if count_ret.is_err:
        return Result.err(count_ret.err_value)

    total = count_ret.ok_value
    ids_ret = repo.get_ids(filter, ExcludeOption(id=id), sort, PageOption(limit=limit, offset=offset), user_id)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    objs_ret = repo.bulk_get(ids=ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value

    data = [replace(o,
        image=create_url(o.image),
        pages=[create_url(p) for p in o.pages],
    ) for o in objs]

    return Result.ok((data, total))


@Result.shield_exception()
def get_pictures(search: str, id: int = 0, channel_id: int = 0, owner_id: int = 0, user_id: int | None = None, is_recommend: bool = False, limit: int = PAGE_SIZE, offset: int = 0) -> Result[tuple[list[PictureData], int], FatalError]:
    repo = injector.get(PictureInterface)
    filter = FilterOption(search=search, publish=True, owner_id=owner_id, channel_id=channel_id, is_recommend=is_recommend)
    sort = SortOption(sort_type=SortType.SCORE)
    count_ret = repo.count(filter)
    if count_ret.is_err:
        return Result.err(count_ret.err_value)

    total = count_ret.ok_value
    ids_ret = repo.get_ids(filter, ExcludeOption(id=id), sort, PageOption(limit=limit, offset=offset), user_id)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    objs_ret = repo.bulk_get(ids=ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    data = [replace(o, image=create_url(o.image)) for o in objs]
    return Result.ok((data, total))


@Result.shield_exception()
def get_chats(search: str, id: int = 0, channel_id: int = 0, owner_id: int = 0, user_id: int | None = None, is_recommend: bool = False, limit: int = PAGE_SIZE, offset: int = 0) -> Result[tuple[list[ChatData], int], FatalError]:
    repo = injector.get(ChatInterface)
    filter = FilterOption(search=search, publish=True, owner_id=owner_id, channel_id=channel_id, is_recommend=is_recommend)
    sort = SortOption(sort_type=SortType.SCORE)
    count_ret = repo.count(filter)
    if count_ret.is_err:
        return Result.err(count_ret.err_value)

    total = count_ret.ok_value
    ids_ret = repo.get_ids(filter, ExcludeOption(id=id), sort, PageOption(limit=limit, offset=offset), user_id)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    objs_ret = repo.bulk_get(ids=ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    return Result.ok((objs, total))


@Result.shield_exception()
def get_video_detail(user_id: int | None, ulid: str, publish: bool = True) -> Result[VideoDetailDTO, FindError]:
    repo = injector.get(VideoInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption(), PageOption(limit=1))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.info("data not found", ulid=ulid)
        return Result.err(NotFoundError("data not found"))

    objs_ret = repo.bulk_get(ids=ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]

    type_no = comment_type_no_map(CommentType.VIDEO)
    comments_ret = get_comments(type_no=type_no, object_id=obj.id, user_id=user_id)
    if comments_ret.is_err:
        return Result.err(comments_ret.err_value)

    comments = comments_ret.ok_value
    is_like = False
    if user_id is not None:
        like_ret = repo.is_liked(obj.id, user_id)
        if like_ret.is_err:
            return Result.err(like_ret.err_value)

        is_like = like_ret.ok_value

    media_user_ret = get_media_user(is_like, obj.channel.id, user_id)
    if media_user_ret.is_err:
        return Result.err(media_user_ret.err_value)

    media_user = media_user_ret.ok_value
    data =VideoDetailDTO(
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
        mediaUser=media_user,
    )

    return Result.ok(data)


@Result.shield_exception()
def get_music_detail(user_id: int | None, ulid: str, publish: bool = True) -> Result[MusicDetailDTO, FindError]:
    repo = injector.get(MusicInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption(), PageOption(limit=1))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.info("data not found", ulid=ulid)
        return Result.err(NotFoundError("data not found"))

    objs_ret = repo.bulk_get(ids=ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]

    type_no = comment_type_no_map(CommentType.MUSIC)
    comments_ret = get_comments(type_no=type_no, object_id=obj.id, user_id=user_id)
    if comments_ret.is_err:
        return Result.err(comments_ret.err_value)

    comments = comments_ret.ok_value
    is_like = False
    if user_id is not None:
        like_ret = repo.is_liked(obj.id, user_id)
        if like_ret.is_err:
            return Result.err(like_ret.err_value)

        is_like = like_ret.ok_value

    media_user_ret = get_media_user(is_like, obj.channel.id, user_id)
    if media_user_ret.is_err:
        return Result.err(media_user_ret.err_value)

    media_user = media_user_ret.ok_value
    is_music_download = False
    if user_id is not None:
        user_ret = get_user_data(user_id=user_id)
        if user_ret.is_err:
            return Result.err(user_ret.err_value)

        user = user_ret.ok_value
        plan = get_plan(user.user_plan.plan) if user is not None else None
        is_music_download = plan is not None and plan.is_music_download

    data =MusicDetailDTO(
        id=obj.id,
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        lyric=obj.lyric,
        music=create_url(obj.music),
        download=obj.download and is_music_download,
        comments=comments,
        hashtags=obj.hashtags,
        read=obj.read,
        like=obj.like,
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        channel=obj.channel,
        mediaUser=media_user,
    )

    return Result.ok(data)


@Result.shield_exception()
def get_blog_detail(user_id: int | None, ulid: str, publish: bool = True) -> Result[BlogDetailDTO, FindError]:
    repo = injector.get(BlogInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption(), PageOption(limit=1))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.info("data not found", ulid=ulid)
        return Result.err(NotFoundError("data not found"))

    objs_ret = repo.bulk_get(ids=ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]

    type_no = comment_type_no_map(CommentType.BLOG)
    comments_ret = get_comments(type_no=type_no, object_id=obj.id, user_id=user_id)
    if comments_ret.is_err:
        return Result.err(comments_ret.err_value)

    comments = comments_ret.ok_value
    is_like = False
    if user_id is not None:
        like_ret = repo.is_liked(obj.id, user_id)
        if like_ret.is_err:
            return Result.err(like_ret.err_value)

        is_like = like_ret.ok_value

    media_user_ret = get_media_user(is_like, obj.channel.id, user_id)
    if media_user_ret.is_err:
        return Result.err(media_user_ret.err_value)

    media_user = media_user_ret.ok_value
    data =BlogDetailDTO(
        id=obj.id,
        ulid=obj.ulid,
        title=obj.title,
        content=obj.content,
        richtext=obj.richtext,
        is_promotion=obj.is_promotion,
        image=create_url(obj.image),
        comments=comments,
        hashtags=obj.hashtags,
        read=obj.read,
        like=obj.like,
        publish=obj.publish,
        created=obj.created,
        updated=obj.updated,
        channel=obj.channel,
        mediaUser=media_user,
    )

    return Result.ok(data)


@Result.shield_exception()
def get_comic_detail(user_id: int | None, ulid: str, publish: bool = True) -> Result[ComicDetailDTO, FindError]:
    repo = injector.get(ComicInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption(), PageOption(limit=1))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.info("data not found", ulid=ulid)
        return Result.err(NotFoundError("data not found"))

    objs_ret = repo.bulk_get(ids=ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]

    type_no = comment_type_no_map(CommentType.COMIC)
    comments_ret = get_comments(type_no=type_no, object_id=obj.id, user_id=user_id)
    if comments_ret.is_err:
        return Result.err(comments_ret.err_value)

    comments = comments_ret.ok_value
    is_like = False
    if user_id is not None:
        like_ret = repo.is_liked(obj.id, user_id)
        if like_ret.is_err:
            return Result.err(like_ret.err_value)

        is_like = like_ret.ok_value

    media_user_ret = get_media_user(is_like, obj.channel.id, user_id)
    if media_user_ret.is_err:
        return Result.err(media_user_ret.err_value)

    media_user = media_user_ret.ok_value
    data =ComicDetailDTO(
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
        mediaUser=media_user,
    )

    return Result.ok(data)


@Result.shield_exception()
def get_picture_detail(user_id: int | None, ulid: str, publish: bool = True) -> Result[PictureDetailDTO, FindError]:
    repo = injector.get(PictureInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption(), PageOption(limit=1))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.info("data not found", ulid=ulid)
        return Result.err(NotFoundError("data not found"))

    objs_ret = repo.bulk_get(ids=ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]

    type_no = comment_type_no_map(CommentType.PICTURE)
    comments_ret = get_comments(type_no=type_no, object_id=obj.id, user_id=user_id)
    if comments_ret.is_err:
        return Result.err(comments_ret.err_value)

    comments = comments_ret.ok_value
    is_like = False
    if user_id is not None:
        like_ret = repo.is_liked(obj.id, user_id)
        if like_ret.is_err:
            return Result.err(like_ret.err_value)

        is_like = like_ret.ok_value

    media_user_ret = get_media_user(is_like, obj.channel.id, user_id)
    if media_user_ret.is_err:
        return Result.err(media_user_ret.err_value)

    media_user = media_user_ret.ok_value
    data =PictureDetailDTO(
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
        mediaUser=media_user,
    )

    return Result.ok(data)


@Result.shield_exception()
def get_chat_detail(user_id: int | None, ulid: str, publish: bool = True) -> Result[ChatDetailDTO, FindError]:
    repo = injector.get(ChatInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid, publish=publish), ExcludeOption(), SortOption(), PageOption(limit=1))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.info("data not found", ulid=ulid)
        return Result.err(NotFoundError("data not found"))

    objs_ret = repo.bulk_get(ids=ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]

    messages_ret = get_messages(chat_id=obj.id)
    if messages_ret.is_err:
        return Result.err(messages_ret.err_value)

    messages = messages_ret.ok_value
    is_like = False
    if user_id is not None:
        like_ret = repo.is_liked(obj.id, user_id)
        if like_ret.is_err:
            return Result.err(like_ret.err_value)

        is_like = like_ret.ok_value

    media_user_ret = get_media_user(is_like, obj.channel.id, user_id)
    if media_user_ret.is_err:
        return Result.err(media_user_ret.err_value)

    media_user = media_user_ret.ok_value
    data =ChatDetailDTO(
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
        mediaUser=media_user,
    )

    return Result.ok(data)


@Result.shield_exception()
def is_public_chat(ulid: str) -> Result[bool, FatalError]:
    repo = injector.get(ChatInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid, publish=True), ExcludeOption(), SortOption(), PageOption(limit=1))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    return Result.ok(len(ids) > 0)


@Result.shield_exception()
def increment_media_read(media_type: MediaType, ulid: str, ip_address: str) -> Result[int, FindError]:
    repo = get_media_repository(media_type)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid, publish=True), ExcludeOption(), SortOption(), PageOption(limit=1))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.info("data not found", ulid=ulid)
        return Result.err(NotFoundError("data not found"))

    objs_ret = repo.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]
    with transaction.atomic():
        access_ret = record_access(ip_address, AccessType(media_type.value), obj.id)
        if access_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(access_ret.err_value)

        is_accessed = access_ret.ok_value
        if not is_accessed:
            return Result.ok(obj.read)

        read_ret = repo.save_read(obj.id)
        if read_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(read_ret.err_value)

        read = read_ret.ok_value
        if read in VIEWS_THRESHOLDS:
            notification_ret = create_views_notification(obj.channel.owner_id, NotificationObjectType(media_type.value), obj.id)
            if notification_ret.is_err:
                transaction.set_rollback(True)
                return Result.err(notification_ret.err_value)

    return Result.ok(read)


@Result.shield_exception()
def create_views_notification(owner_id: int, object_type: NotificationObjectType, object_id: int) -> Result[None, FatalError]:
    repo = injector.get(NotificationInterface)
    delete_ret = repo.delete(NotificationTypeNo.VIEWS, object_type, object_id, owner_id)
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    create_ret = create_notification(owner_id, owner_id, NotificationTypeNo.VIEWS, object_id, object_type)
    if create_ret.is_err:
        return Result.err(create_ret.err_value)

    return Result.ok(None)
