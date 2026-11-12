from myus.src.domain.interface.category.data import CategoryData
from myus.src.domain.interface.category.interface import CategoryInterface
from myus.src.domain.interface.media.video.data import VideoData
from myus.src.domain.interface.media.video.interface import VideoInterface
from myus.src.domain.interface.media.music.data import MusicData
from myus.src.domain.interface.media.music.interface import MusicInterface
from myus.src.domain.interface.media.blog.data import BlogData
from myus.src.domain.interface.media.blog.interface import BlogInterface
from myus.src.domain.interface.media.comic.data import ComicData
from myus.src.domain.interface.media.comic.interface import ComicInterface
from myus.src.domain.interface.media.picture.data import PictureData
from myus.src.domain.interface.media.picture.interface import PictureInterface
from myus.src.domain.interface.media.chat.data import ChatData
from myus.src.domain.interface.media.chat.interface import ChatInterface
from myus.src.injectors.container import injector
from myus.src.usecase.notification._convert import delete_notification_data
from myus.utils.common.result import FatalError, Result
from myus.utils.enum.media import MediaType
from myus.utils.enum.notification import NotificationObjectType


@Result.shield_exception()
def save_video_data(data: VideoData, category_data: CategoryData) -> Result[None, FatalError]:
    repo = injector.get(VideoInterface)
    category_repo = injector.get(CategoryInterface)
    save_ret = repo.bulk_save([data])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    category_ret = category_repo.bulk_save(MediaType.VIDEO, data.id, [category_data])
    if category_ret.is_err:
        return Result.err(category_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def save_music_data(data: MusicData, category_data: CategoryData) -> Result[None, FatalError]:
    repo = injector.get(MusicInterface)
    category_repo = injector.get(CategoryInterface)
    save_ret = repo.bulk_save([data])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    category_ret = category_repo.bulk_save(MediaType.MUSIC, data.id, [category_data])
    if category_ret.is_err:
        return Result.err(category_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def save_blog_data(data: BlogData, category_data: CategoryData) -> Result[None, FatalError]:
    repo = injector.get(BlogInterface)
    category_repo = injector.get(CategoryInterface)
    save_ret = repo.bulk_save([data])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    category_ret = category_repo.bulk_save(MediaType.BLOG, data.id, [category_data])
    if category_ret.is_err:
        return Result.err(category_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def save_comic_data(data: ComicData, category_data: CategoryData) -> Result[None, FatalError]:
    repo = injector.get(ComicInterface)
    category_repo = injector.get(CategoryInterface)
    save_ret = repo.bulk_save([data])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    category_ret = category_repo.bulk_save(MediaType.COMIC, data.id, [category_data])
    if category_ret.is_err:
        return Result.err(category_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def save_picture_data(data: PictureData, category_data: CategoryData) -> Result[None, FatalError]:
    repo = injector.get(PictureInterface)
    category_repo = injector.get(CategoryInterface)
    save_ret = repo.bulk_save([data])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    category_ret = category_repo.bulk_save(MediaType.PICTURE, data.id, [category_data])
    if category_ret.is_err:
        return Result.err(category_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def save_chat_data(data: ChatData, category_data: CategoryData) -> Result[None, FatalError]:
    repo = injector.get(ChatInterface)
    category_repo = injector.get(CategoryInterface)
    save_ret = repo.bulk_save([data])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    category_ret = category_repo.bulk_save(MediaType.CHAT, data.id, [category_data])
    if category_ret.is_err:
        return Result.err(category_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_video_data(ids: list[int]) -> Result[None, FatalError]:
    repo = injector.get(VideoInterface)
    delete_ret = repo.bulk_delete(ids)
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    notification_ret = delete_notification_data(NotificationObjectType.VIDEO, ids)
    if notification_ret.is_err:
        return Result.err(notification_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_music_data(ids: list[int]) -> Result[None, FatalError]:
    repo = injector.get(MusicInterface)
    delete_ret = repo.bulk_delete(ids)
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    notification_ret = delete_notification_data(NotificationObjectType.MUSIC, ids)
    if notification_ret.is_err:
        return Result.err(notification_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_blog_data(ids: list[int]) -> Result[None, FatalError]:
    repo = injector.get(BlogInterface)
    delete_ret = repo.bulk_delete(ids)
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    notification_ret = delete_notification_data(NotificationObjectType.BLOG, ids)
    if notification_ret.is_err:
        return Result.err(notification_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_comic_data(ids: list[int]) -> Result[None, FatalError]:
    repo = injector.get(ComicInterface)
    delete_ret = repo.bulk_delete(ids)
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    notification_ret = delete_notification_data(NotificationObjectType.COMIC, ids)
    if notification_ret.is_err:
        return Result.err(notification_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_picture_data(ids: list[int]) -> Result[None, FatalError]:
    repo = injector.get(PictureInterface)
    delete_ret = repo.bulk_delete(ids)
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    notification_ret = delete_notification_data(NotificationObjectType.PICTURE, ids)
    if notification_ret.is_err:
        return Result.err(notification_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_chat_data(ids: list[int], reply_ids: list[int]) -> Result[None, FatalError]:
    repo = injector.get(ChatInterface)
    delete_ret = repo.bulk_delete(ids)
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    chat_notification_ret = delete_notification_data(NotificationObjectType.CHAT, ids)
    if chat_notification_ret.is_err:
        return Result.err(chat_notification_ret.err_value)

    message_notification_ret = delete_notification_data(NotificationObjectType.MESSAGE, reply_ids)
    if message_notification_ret.is_err:
        return Result.err(message_notification_ret.err_value)

    return Result.ok(None)
