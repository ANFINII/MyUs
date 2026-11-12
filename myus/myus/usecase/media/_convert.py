from typing import assert_never
from myus.domain.category.data import CategoryData
from myus.domain.category.interface import CategoryInterface
from myus.domain.media.blog.data import BlogData
from myus.domain.media.blog.interface import BlogInterface
from myus.domain.media.chat.data import ChatData
from myus.domain.media.chat.interface import ChatInterface
from myus.domain.media.comic.data import ComicData
from myus.domain.media.comic.interface import ComicInterface
from myus.domain.media.music.data import MusicData
from myus.domain.media.music.interface import MusicInterface
from myus.domain.media.picture.data import PictureData
from myus.domain.media.picture.interface import PictureInterface
from myus.domain.media.video.data import VideoData
from myus.domain.media.video.interface import VideoInterface
from myus.domain.subscribe.interface import FilterOption, SortOption, SubscribeInterface
from myus.injectors.container import injector
from myus.utils.common.result import FatalError, Result
from myus.utils.enum.access_log import AccessType
from myus.utils.enum.media import MediaType
from myus.utils.enum.notification import NotificationObjectType, NotificationTypeNo
from ..access_log._convert import save_access_data
from ..dto.user import MediaUserDTO
from ..notification._convert import create_notification_data, delete_notification_data


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
def get_media_user_data(is_like: bool, channel_id: int, user_id: int | None) -> Result[MediaUserDTO, FatalError]:
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
    access_ret = save_access_data(ip_address, AccessType(media_type.value), media_id)
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
        notification_ret = create_views_notification_data(owner_id, NotificationObjectType(media_type.value), media_id)
        if notification_ret.is_err:
            return Result.err(notification_ret.err_value)

    return Result.ok(new_read)


@Result.shield_exception()
def create_views_notification_data(owner_id: int, object_type: NotificationObjectType, object_id: int) -> Result[None, FatalError]:
    delete_ret = delete_notification_data(object_type, [object_id], NotificationTypeNo.VIEWS, owner_id)
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    create_ret = create_notification_data(owner_id, owner_id, NotificationTypeNo.VIEWS, object_id, object_type)
    if create_ret.is_err:
        return Result.err(create_ret.err_value)

    return Result.ok(None)
