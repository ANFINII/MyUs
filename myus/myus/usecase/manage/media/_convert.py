from dataclasses import replace
from myus.domain.category.data import CategoryData
from myus.domain.category.interface import CategoryInterface
from myus.domain.media.audio.data import AudioData
from myus.domain.media.audio.interface import AudioInterface
from myus.domain.media.blog.data import BlogData
from myus.domain.media.blog.interface import BlogInterface
from myus.domain.media.chat.data import ChatData
from myus.domain.media.chat.interface import ChatInterface
from myus.domain.media.comic.data import ComicData
from myus.domain.media.comic.interface import ComicInterface
from myus.domain.media.picture.data import PictureData
from myus.domain.media.picture.interface import PictureInterface
from myus.domain.media.video.data import VideoData
from myus.domain.media.video.interface import VideoInterface
from myus.domain.payment.product.data import ProductData
from myus.injectors.container import injector
from myus.utils.common.result import FatalError, Result
from myus.utils.enum.media import CommentTypeNo, MediaType
from myus.utils.enum.notification import NotificationObjectType
from myus.utils.enum.payment import ProductType
from ...comment._convert import delete_comments_data
from ...notification._convert import delete_notification_data
from ...payment._convert import delete_products_data, save_product_data
from ...series._convert import delete_series_media_data


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
def save_audio_data(data: AudioData, category_data: CategoryData) -> Result[None, FatalError]:
    repo = injector.get(AudioInterface)
    category_repo = injector.get(CategoryInterface)
    save_ret = repo.bulk_save([data])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    category_ret = category_repo.bulk_save(MediaType.AUDIO, data.id, [category_data])
    if category_ret.is_err:
        return Result.err(category_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def save_blog_data(data: BlogData, category_data: CategoryData, product: ProductData | None) -> Result[None, FatalError]:
    repo = injector.get(BlogInterface)
    category_repo = injector.get(CategoryInterface)
    save_ret = repo.bulk_save([data])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    category_ret = category_repo.bulk_save(MediaType.BLOG, data.id, [category_data])
    if category_ret.is_err:
        return Result.err(category_ret.err_value)

    product_ret = save_product_data(product) if product is not None else delete_products_data(ProductType.BLOG, [data.id])
    if product_ret.is_err:
        return Result.err(product_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def save_hires_data(data: AudioData, product: ProductData) -> Result[None, FatalError]:
    repo = injector.get(AudioInterface)
    save_ret = repo.bulk_save([data])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    product_ret = save_product_data(product)
    if product_ret.is_err:
        return Result.err(product_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_hires_data(data: AudioData) -> Result[None, FatalError]:
    repo = injector.get(AudioInterface)
    save_ret = repo.bulk_save([replace(data, hires=None)])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    product_ret = delete_products_data(ProductType.HIRES, [data.id])
    if product_ret.is_err:
        return Result.err(product_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def save_comic_data(data: ComicData, category_data: CategoryData, product: ProductData | None) -> Result[None, FatalError]:
    repo = injector.get(ComicInterface)
    category_repo = injector.get(CategoryInterface)
    save_ret = repo.bulk_save([data])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    category_ret = category_repo.bulk_save(MediaType.COMIC, data.id, [category_data])
    if category_ret.is_err:
        return Result.err(category_ret.err_value)

    product_ret = save_product_data(product) if product is not None else delete_products_data(ProductType.COMIC, [data.id])
    if product_ret.is_err:
        return Result.err(product_ret.err_value)

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

    comment_ret = delete_comments_data(CommentTypeNo.VIDEO, ids)
    if comment_ret.is_err:
        return Result.err(comment_ret.err_value)

    series_ret = delete_series_media_data(MediaType.VIDEO, ids)
    if series_ret.is_err:
        return Result.err(series_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_audio_data(ids: list[int]) -> Result[None, FatalError]:
    product_ret = delete_products_data(ProductType.HIRES, ids)
    if product_ret.is_err:
        return Result.err(product_ret.err_value)

    repo = injector.get(AudioInterface)
    delete_ret = repo.bulk_delete(ids)
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    notification_ret = delete_notification_data(NotificationObjectType.AUDIO, ids)
    if notification_ret.is_err:
        return Result.err(notification_ret.err_value)

    comment_ret = delete_comments_data(CommentTypeNo.AUDIO, ids)
    if comment_ret.is_err:
        return Result.err(comment_ret.err_value)

    series_ret = delete_series_media_data(MediaType.AUDIO, ids)
    if series_ret.is_err:
        return Result.err(series_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_blog_data(ids: list[int]) -> Result[None, FatalError]:
    product_ret = delete_products_data(ProductType.BLOG, ids)
    if product_ret.is_err:
        return Result.err(product_ret.err_value)

    repo = injector.get(BlogInterface)
    delete_ret = repo.bulk_delete(ids)
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    notification_ret = delete_notification_data(NotificationObjectType.BLOG, ids)
    if notification_ret.is_err:
        return Result.err(notification_ret.err_value)

    comment_ret = delete_comments_data(CommentTypeNo.BLOG, ids)
    if comment_ret.is_err:
        return Result.err(comment_ret.err_value)

    series_ret = delete_series_media_data(MediaType.BLOG, ids)
    if series_ret.is_err:
        return Result.err(series_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_comic_data(ids: list[int]) -> Result[None, FatalError]:
    product_ret = delete_products_data(ProductType.COMIC, ids)
    if product_ret.is_err:
        return Result.err(product_ret.err_value)

    repo = injector.get(ComicInterface)
    delete_ret = repo.bulk_delete(ids)
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    notification_ret = delete_notification_data(NotificationObjectType.COMIC, ids)
    if notification_ret.is_err:
        return Result.err(notification_ret.err_value)

    comment_ret = delete_comments_data(CommentTypeNo.COMIC, ids)
    if comment_ret.is_err:
        return Result.err(comment_ret.err_value)

    series_ret = delete_series_media_data(MediaType.COMIC, ids)
    if series_ret.is_err:
        return Result.err(series_ret.err_value)

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

    comment_ret = delete_comments_data(CommentTypeNo.PICTURE, ids)
    if comment_ret.is_err:
        return Result.err(comment_ret.err_value)

    series_ret = delete_series_media_data(MediaType.PICTURE, ids)
    if series_ret.is_err:
        return Result.err(series_ret.err_value)

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

    series_ret = delete_series_media_data(MediaType.CHAT, ids)
    if series_ret.is_err:
        return Result.err(series_ret.err_value)

    return Result.ok(None)
