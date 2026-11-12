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
from myus.injectors.container import injector
from myus.utils.common.result import FatalError, Result
from myus.utils.enum.media import MediaType
from myus.utils.enum.notification import NotificationObjectType
from ...notification._convert import delete_notification_data


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
