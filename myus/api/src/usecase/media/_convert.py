from typing import assert_never
from api.src.domain.interface.category.data import CategoryData
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
from api.src.domain.interface.notification.interface import NotificationInterface
from api.src.domain.interface.subscribe.interface import FilterOption, SortOption, SubscribeInterface
from api.src.injectors.container import injector
from api.src.types.dto.user import MediaUserDTO
from api.src.usecase.access_log import record_access
from api.src.usecase.notification import create_notification
from api.utils.common.result import FatalError, Result
from api.utils.enum.access_log import AccessType
from api.utils.enum.media import MediaType
from api.utils.enum.notification import NotificationObjectType, NotificationTypeNo


type MediaInterfaceType = VideoInterface | MusicInterface | BlogInterface | ComicInterface | PictureInterface | ChatInterface

VIEWS_THRESHOLDS = (10000, 100000, 1000000, 10000000, 100000000, 1000000000)


def get_media_repository(media_type: MediaType) -> MediaInterfaceType:
    match media_type:
        case MediaType.VIDEO:
            return injector.get(VideoInterface)
        case MediaType.MUSIC:
            return injector.get(MusicInterface)
        case MediaType.BLOG:
            return injector.get(BlogInterface)
        case MediaType.COMIC:
            return injector.get(ComicInterface)
        case MediaType.PICTURE:
            return injector.get(PictureInterface)
        case MediaType.CHAT:
            return injector.get(ChatInterface)
        case _:
            assert_never(media_type)


@Result.shield_exception()
def get_media_user(is_like: bool, channel_id: int, user_id: int | None) -> Result[MediaUserDTO, FatalError]:
    subscribe_repo = injector.get(SubscribeInterface)
    subscribe = None
    if user_id is not None:
        ids_ret = subscribe_repo.get_ids(FilterOption(user_id=user_id, channel_id=channel_id), SortOption())
        if ids_ret.is_err:
            return Result.err(ids_ret.err_value)

        ids = ids_ret.ok_value
        subscribes_ret = subscribe_repo.bulk_get(ids)
        if subscribes_ret.is_err:
            return Result.err(subscribes_ret.err_value)

        subscribes = subscribes_ret.ok_value
        subscribe = subscribes[0] if len(subscribes) > 0 else None

    data = MediaUserDTO(
        is_like=is_like,
        is_subscribe=subscribe.is_subscribe if subscribe else False,
    )

    return Result.ok(data)


@Result.shield_exception()
def create_video_data(data: VideoData, category_data: CategoryData) -> Result[int, FatalError]:
    repo = injector.get(VideoInterface)
    category_repo = injector.get(CategoryInterface)
    ids_ret = repo.bulk_save([data])
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    new_ids = ids_ret.ok_value
    assert len(new_ids) == 1, "作成に失敗しました"
    category_ret = category_repo.bulk_save(MediaType.VIDEO, new_ids[0], [category_data])
    if category_ret.is_err:
        return Result.err(category_ret.err_value)

    return Result.ok(new_ids[0])


@Result.shield_exception()
def create_music_data(data: MusicData, category_data: CategoryData) -> Result[int, FatalError]:
    repo = injector.get(MusicInterface)
    category_repo = injector.get(CategoryInterface)
    ids_ret = repo.bulk_save([data])
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    new_ids = ids_ret.ok_value
    assert len(new_ids) == 1, "作成に失敗しました"
    category_ret = category_repo.bulk_save(MediaType.MUSIC, new_ids[0], [category_data])
    if category_ret.is_err:
        return Result.err(category_ret.err_value)

    return Result.ok(new_ids[0])


@Result.shield_exception()
def create_blog_data(data: BlogData, category_data: CategoryData) -> Result[int, FatalError]:
    repo = injector.get(BlogInterface)
    category_repo = injector.get(CategoryInterface)
    ids_ret = repo.bulk_save([data])
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    new_ids = ids_ret.ok_value
    assert len(new_ids) == 1, "作成に失敗しました"
    category_ret = category_repo.bulk_save(MediaType.BLOG, new_ids[0], [category_data])
    if category_ret.is_err:
        return Result.err(category_ret.err_value)

    return Result.ok(new_ids[0])


@Result.shield_exception()
def create_comic_data(data: ComicData, category_data: CategoryData) -> Result[int, FatalError]:
    repo = injector.get(ComicInterface)
    category_repo = injector.get(CategoryInterface)
    ids_ret = repo.bulk_save([data])
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    new_ids = ids_ret.ok_value
    assert len(new_ids) == 1, "作成に失敗しました"
    category_ret = category_repo.bulk_save(MediaType.COMIC, new_ids[0], [category_data])
    if category_ret.is_err:
        return Result.err(category_ret.err_value)

    return Result.ok(new_ids[0])


@Result.shield_exception()
def create_picture_data(data: PictureData, category_data: CategoryData) -> Result[int, FatalError]:
    repo = injector.get(PictureInterface)
    category_repo = injector.get(CategoryInterface)
    ids_ret = repo.bulk_save([data])
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    new_ids = ids_ret.ok_value
    assert len(new_ids) == 1, "作成に失敗しました"
    category_ret = category_repo.bulk_save(MediaType.PICTURE, new_ids[0], [category_data])
    if category_ret.is_err:
        return Result.err(category_ret.err_value)

    return Result.ok(new_ids[0])


@Result.shield_exception()
def create_chat_data(data: ChatData, category_data: CategoryData) -> Result[int, FatalError]:
    repo = injector.get(ChatInterface)
    category_repo = injector.get(CategoryInterface)
    ids_ret = repo.bulk_save([data])
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    new_ids = ids_ret.ok_value
    assert len(new_ids) == 1, "作成に失敗しました"
    category_ret = category_repo.bulk_save(MediaType.CHAT, new_ids[0], [category_data])
    if category_ret.is_err:
        return Result.err(category_ret.err_value)

    return Result.ok(new_ids[0])


@Result.shield_exception()
def save_read_data(media_type: MediaType, media_id: int, read: int, owner_id: int, ip_address: str) -> Result[int, FatalError]:
    repo = get_media_repository(media_type)
    access_ret = record_access(ip_address, AccessType(media_type.value), media_id)
    if access_ret.is_err:
        return Result.err(access_ret.err_value)

    is_accessed = access_ret.ok_value
    if not is_accessed:
        return Result.ok(read)

    read_ret = repo.save_read(media_id)
    if read_ret.is_err:
        return Result.err(read_ret.err_value)

    new_read = read_ret.ok_value
    if new_read in VIEWS_THRESHOLDS:
        notification_ret = create_views_notification(owner_id, NotificationObjectType(media_type.value), media_id)
        if notification_ret.is_err:
            return Result.err(notification_ret.err_value)

    return Result.ok(new_read)


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
