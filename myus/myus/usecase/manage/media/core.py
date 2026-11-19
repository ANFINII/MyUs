from dataclasses import replace
from ninja import UploadedFile
from django.utils import timezone
from myus.domain.media.blog.data import BlogData
from myus.domain.media.blog.interface import BlogInterface
from myus.domain.media.chat.data import ChatData
from myus.domain.media.chat.interface import ChatInterface
from myus.domain.media.comic.data import ComicData
from myus.domain.media.comic.interface import ComicInterface
from myus.domain.media.hires.data import MusicHiresData
from myus.domain.media.common import MEDIA_PAGE_SIZE, FilterOption, PageOption, SortOption
from myus.domain.media.music.data import MusicData
from myus.domain.media.music.interface import MusicInterface
from myus.domain.media.picture.data import PictureData
from myus.domain.media.picture.interface import PictureInterface
from myus.domain.media.video.data import VideoData
from myus.domain.media.video.interface import VideoInterface
from myus.domain.message.interface import FilterOption as MessageFilterOption, MessageInterface, PageOption as MessagePageOption, SortOption as MessageSortOption
from myus.domain.payment.data import Money
from myus.domain.payment.product.data import ProductData
from myus.injectors.container import injector
from myus.utils.common.logger import log
from myus.utils.common.result import FatalError, FindError, ForbiddenError, InputError, NotFoundError, Result, ValidationError, WriteError
from myus.utils.enum.media import EncodeStatus
from myus.utils.enum.notification import NotificationObjectType, NotificationTypeNo
from myus.utils.enum.payment import ProductType
from myus.utils.enum.upload import ImageUpload, MediaUpload
from myus.utils.functions.common import create_url
from myus.utils.functions.convert.audio_converter import measure_music_gain, probe_audio
from myus.utils.functions.media import probe_upload, save_upload, validate_uploads
from myus.utils.functions.transaction import atomic_result
from ._convert import save_video_data, save_music_data, save_music_hires_data, save_blog_data, save_comic_data, save_picture_data, save_chat_data, delete_video_data, delete_music_data, delete_music_hires_data, delete_blog_data, delete_comic_data, delete_picture_data, delete_chat_data
from ...category._convert import get_category_data
from ...dto.media import VideoUpdateDTO, MusicUpdateDTO, BlogUpdateDTO, ComicUpdateDTO, PictureUpdateDTO, ChatUpdateDTO
from ...media._convert import get_music_hires_data
from ...notification._convert import create_publish_notification_data
from ...payment._convert import get_product_data, get_product_purchase_ids_data, get_purchase_ids_data, get_seller_currency_data


@Result.shield_exception()
def get_manage_videos(user_id: int, search: str, channel_ulid: str = "", limit: int = MEDIA_PAGE_SIZE, offset: int = 0) -> Result[tuple[list[VideoData], int], FatalError]:
    repo = injector.get(VideoInterface)
    filter = FilterOption(search=search, owner_id=user_id, channel_ulid=channel_ulid)
    count_ret = repo.count(filter)
    if count_ret.is_err:
        return Result.err(count_ret.err_value)

    total = count_ret.ok_value
    ids_ret = repo.get_ids(filter, SortOption(), PageOption(limit=limit, offset=offset))
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
def get_manage_video(user_id: int, ulid: str) -> Result[VideoData, FindError]:
    repo = injector.get(VideoInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid, owner_id=user_id), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.info("not found", ulid=ulid, user_id=user_id)
        return Result.err(NotFoundError("error.mediaNotFound"))

    objs_ret = repo.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]
    return Result.ok(replace(obj,
        image=create_url(obj.image),
        video=create_url(obj.video),
        convert=create_url(obj.convert),
    ))


@Result.shield_exception()
def update_manage_video(user_id: int, ulid: str, input: VideoUpdateDTO, image: UploadedFile | None = None, video: UploadedFile | None = None) -> Result[None, WriteError]:
    upload_ret = validate_uploads([(image, ImageUpload.VIDEO), (video, MediaUpload.VIDEO)])
    if upload_ret.is_err:
        return Result.err(upload_ret.err_value)

    repo = injector.get(VideoInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.warning("not found", ulid=ulid)
        return Result.err(NotFoundError("error.saveFailed"))

    objs_ret = repo.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]
    owner_id = obj.channel.owner_id
    if owner_id != user_id:
        log.error("owner mismatch", ulid=ulid, user_id=user_id, owner_id=owner_id)
        return Result.err(ForbiddenError("error.saveFailed"))

    update_data = replace(obj, title=input.title, content=input.content, publish=input.publish, publish_at=input.publish_at)
    if image is not None:
        update_data = replace(update_data, image=save_upload(image, ImageUpload.VIDEO, obj.channel.ulid))
    if video is not None:
        if obj.encode_status != EncodeStatus.FAILED:
            log.warning("not encode failed", ulid=ulid)
            return Result.err(ValidationError("error.saveFailed"))
        update_data = replace(update_data, video=save_upload(video, MediaUpload.VIDEO, obj.channel.ulid), convert="", encode_status=EncodeStatus.ENCODING)

    category_data_ret = get_category_data(input.category_ulid)
    if category_data_ret.is_err:
        return Result.err(category_data_ret.err_value)

    category_data = category_data_ret.ok_value

    save_ret = atomic_result(lambda: save_video_data(update_data, category_data))
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    if not obj.publish and input.publish and obj.convert != "":
        notification_ret = create_publish_notification_data(user_id, NotificationTypeNo.VIDEO, obj.id, NotificationObjectType.VIDEO)
        if notification_ret.is_err:
            return Result.err(notification_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_manage_video(user_id: int, ulids: list[str]) -> Result[None, FindError]:
    repo = injector.get(VideoInterface)
    ids_ret = repo.get_ids(FilterOption(ulids=ulids, owner_id=user_id), SortOption(), PageOption(limit=len(ulids)))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    delete_ids = ids_ret.ok_value
    if len(delete_ids) != len(set(ulids)):
        log.warning("not found or owner mismatch", ulids=ulids, user_id=user_id)
        return Result.err(NotFoundError("error.deleteFailed"))

    delete_ret = atomic_result(lambda: delete_video_data(delete_ids))
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def get_manage_musics(user_id: int, search: str, channel_ulid: str = "", limit: int = MEDIA_PAGE_SIZE, offset: int = 0) -> Result[tuple[list[MusicData], int], FatalError]:
    repo = injector.get(MusicInterface)
    filter = FilterOption(search=search, owner_id=user_id, channel_ulid=channel_ulid)
    count_ret = repo.count(filter)
    if count_ret.is_err:
        return Result.err(count_ret.err_value)

    total = count_ret.ok_value
    ids_ret = repo.get_ids(filter, SortOption(), PageOption(limit=limit, offset=offset))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    objs_ret = repo.bulk_get(ids=ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value

    data = [replace(o, image=create_url(o.image), music=create_url(o.music)) for o in objs]
    return Result.ok((data, total))


@Result.shield_exception()
def get_manage_music(user_id: int, ulid: str) -> Result[tuple[MusicData, MusicHiresData | None, ProductData | None], FindError]:
    repo = injector.get(MusicInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid, owner_id=user_id), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.info("not found", ulid=ulid, user_id=user_id)
        return Result.err(NotFoundError("error.mediaNotFound"))

    objs_ret = repo.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]
    hires_ret = get_music_hires_data(obj.id)
    if hires_ret.is_err:
        return Result.err(hires_ret.err_value)

    hires = hires_ret.ok_value
    product_ret = get_product_data(ProductType.MUSIC_HIRES, obj.id)
    if product_ret.is_err:
        return Result.err(product_ret.err_value)

    product = product_ret.ok_value
    return Result.ok((replace(obj, image=create_url(obj.image), music=create_url(obj.music)), hires, product))


@Result.shield_exception()
def update_manage_music(user_id: int, ulid: str, input: MusicUpdateDTO, image: UploadedFile | None = None, music: UploadedFile | None = None) -> Result[None, WriteError]:
    upload_ret = validate_uploads([(image, ImageUpload.MUSIC), (music, MediaUpload.MUSIC)])
    if upload_ret.is_err:
        return Result.err(upload_ret.err_value)

    repo = injector.get(MusicInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.warning("not found", ulid=ulid)
        return Result.err(NotFoundError("error.saveFailed"))

    objs_ret = repo.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]
    owner_id = obj.channel.owner_id
    if owner_id != user_id:
        log.error("owner mismatch", ulid=ulid, user_id=user_id, owner_id=owner_id)
        return Result.err(ForbiddenError("error.saveFailed"))

    update_data = replace(obj, title=input.title, content=input.content, lyric=input.lyric, publish=input.publish, publish_at=input.publish_at)
    if image is not None:
        update_data = replace(update_data, image=save_upload(image, ImageUpload.MUSIC, obj.channel.ulid))
    if music is not None:
        music_path = save_upload(music, MediaUpload.MUSIC, obj.channel.ulid)
        update_data = replace(update_data, music=music_path, gain=measure_music_gain(music_path))
    category_data_ret = get_category_data(input.category_ulid)
    if category_data_ret.is_err:
        return Result.err(category_data_ret.err_value)

    category_data = category_data_ret.ok_value

    save_ret = atomic_result(lambda: save_music_data(update_data, category_data))
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    if not obj.publish and input.publish:
        notification_ret = create_publish_notification_data(user_id, NotificationTypeNo.MUSIC, obj.id, NotificationObjectType.MUSIC)
        if notification_ret.is_err:
            return Result.err(notification_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_manage_music(user_id: int, ulids: list[str]) -> Result[None, InputError]:
    repo = injector.get(MusicInterface)
    ids_ret = repo.get_ids(FilterOption(ulids=ulids, owner_id=user_id), SortOption(), PageOption(limit=len(ulids)))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    delete_ids = ids_ret.ok_value
    if len(delete_ids) != len(set(ulids)):
        log.warning("not found or owner mismatch", ulids=ulids, user_id=user_id)
        return Result.err(NotFoundError("error.deleteFailed"))

    purchase_ids_ret = get_product_purchase_ids_data(ProductType.MUSIC_HIRES, delete_ids)
    if purchase_ids_ret.is_err:
        return Result.err(purchase_ids_ret.err_value)

    purchase_ids = purchase_ids_ret.ok_value
    if len(purchase_ids) > 0:
        log.warning("purchased", ulids=ulids, user_id=user_id)
        return Result.err(ValidationError("error.deletePurchased"))

    delete_ret = atomic_result(lambda: delete_music_data(delete_ids))
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def update_manage_music_hires(user_id: int, ulid: str, price: int, hires: UploadedFile | None = None) -> Result[None, WriteError]:
    upload_ret = validate_uploads([(hires, MediaUpload.HIRES)])
    if upload_ret.is_err:
        return Result.err(upload_ret.err_value)

    repo = injector.get(MusicInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.warning("not found", ulid=ulid)
        return Result.err(NotFoundError("error.saveFailed"))

    objs_ret = repo.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]
    owner_id = obj.channel.owner_id
    if owner_id != user_id:
        log.error("owner mismatch", ulid=ulid, user_id=user_id, owner_id=owner_id)
        return Result.err(ForbiddenError("error.saveFailed"))

    currency_ret = get_seller_currency_data(user_id)
    if currency_ret.is_err:
        return Result.err(currency_ret.err_value)

    currency = currency_ret.ok_value
    hires_ret = get_music_hires_data(obj.id)
    if hires_ret.is_err:
        return Result.err(hires_ret.err_value)

    current = hires_ret.ok_value
    product_ret = get_product_data(ProductType.MUSIC_HIRES, obj.id)
    if product_ret.is_err:
        return Result.err(product_ret.err_value)

    product = product_ret.ok_value
    if hires is None:
        if current is None:
            log.error("hires required", ulid=ulid)
            return Result.err(FatalError("hires required"))

        save_data = current
    else:
        audio = probe_upload(hires, probe_audio)
        path = save_upload(hires, MediaUpload.HIRES, obj.channel.ulid)
        save_data = MusicHiresData(
            id=current.id if current is not None else 0,
            music_id=obj.id,
            file=path,
            sample_rate=audio.sample_rate,
            bit_depth=audio.bit_depth,
        )

    save_product = ProductData(
        id=product.id if product is not None else 0,
        ulid=product.ulid if product is not None else "",
        seller_id=user_id,
        product_type=ProductType.MUSIC_HIRES,
        object_id=obj.id,
        price=Money(amount=price, currency=currency),
    )
    save_ret = atomic_result(lambda: save_music_hires_data(save_data, save_product))
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_manage_music_hires(user_id: int, ulid: str) -> Result[None, InputError]:
    repo = injector.get(MusicInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid, owner_id=user_id), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.warning("not found or owner mismatch", ulid=ulid, user_id=user_id)
        return Result.err(NotFoundError("error.deleteFailed"))

    hires_ret = get_music_hires_data(ids[0])
    if hires_ret.is_err:
        return Result.err(hires_ret.err_value)

    hires = hires_ret.ok_value
    if hires is None:
        return Result.ok(None)

    purchase_ids_ret = get_product_purchase_ids_data(ProductType.MUSIC_HIRES, [hires.music_id])
    if purchase_ids_ret.is_err:
        return Result.err(purchase_ids_ret.err_value)

    purchase_ids = purchase_ids_ret.ok_value
    if len(purchase_ids) > 0:
        log.warning("purchased", ulid=ulid, user_id=user_id)
        return Result.err(ValidationError("error.saleStopPurchased"))

    delete_ret = atomic_result(lambda: delete_music_hires_data(hires))
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def get_manage_blogs(user_id: int, search: str, channel_ulid: str = "", limit: int = MEDIA_PAGE_SIZE, offset: int = 0) -> Result[tuple[list[BlogData], int], FatalError]:
    repo = injector.get(BlogInterface)
    filter = FilterOption(search=search, owner_id=user_id, channel_ulid=channel_ulid)
    count_ret = repo.count(filter)
    if count_ret.is_err:
        return Result.err(count_ret.err_value)

    total = count_ret.ok_value
    ids_ret = repo.get_ids(filter, SortOption(), PageOption(limit=limit, offset=offset))
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
def get_manage_blog(user_id: int, ulid: str) -> Result[tuple[BlogData, ProductData | None], FindError]:
    repo = injector.get(BlogInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid, owner_id=user_id), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.info("not found", ulid=ulid, user_id=user_id)
        return Result.err(NotFoundError("error.mediaNotFound"))

    objs_ret = repo.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]
    product_ret = get_product_data(ProductType.BLOG, obj.id)
    if product_ret.is_err:
        return Result.err(product_ret.err_value)

    product = product_ret.ok_value
    return Result.ok((replace(obj, image=create_url(obj.image)), product))


@Result.shield_exception()
def update_manage_blog(user_id: int, ulid: str, input: BlogUpdateDTO, image: UploadedFile | None = None) -> Result[None, WriteError]:
    upload_ret = validate_uploads([(image, ImageUpload.BLOG)])
    if upload_ret.is_err:
        return Result.err(upload_ret.err_value)

    repo = injector.get(BlogInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.warning("not found", ulid=ulid)
        return Result.err(NotFoundError("error.saveFailed"))

    objs_ret = repo.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]
    owner_id = obj.channel.owner_id
    if owner_id != user_id:
        log.error("owner mismatch", ulid=ulid, user_id=user_id, owner_id=owner_id)
        return Result.err(ForbiddenError("error.saveFailed"))

    product_ret = get_product_data(ProductType.BLOG, obj.id)
    if product_ret.is_err:
        return Result.err(product_ret.err_value)

    product = product_ret.ok_value
    if len(input.paid_text) == 0 and product is not None:
        purchase_ids_ret = get_purchase_ids_data([product.id])
        if purchase_ids_ret.is_err:
            return Result.err(purchase_ids_ret.err_value)

        purchase_ids = purchase_ids_ret.ok_value
        if len(purchase_ids) > 0:
            log.warning("purchased", ulid=ulid, user_id=user_id)
            return Result.err(ValidationError("error.saleStopPurchased"))

    save_product = product if len(input.paid_text) > 0 else None
    is_paid_changed = input.paid_text != obj.paid_text or product is None or input.price != product.price.amount
    if len(input.paid_text) > 0 and is_paid_changed:
        currency_ret = get_seller_currency_data(user_id)
        if currency_ret.is_err:
            return Result.err(currency_ret.err_value)

        currency = currency_ret.ok_value
        save_product = ProductData(
            id=product.id if product is not None else 0,
            ulid=product.ulid if product is not None else "",
            seller_id=user_id,
            product_type=ProductType.BLOG,
            object_id=obj.id,
            price=Money(amount=input.price, currency=currency),
        )

    update_data = replace(obj, title=input.title, content=input.content, richtext=input.richtext, paid_text=input.paid_text, publish=input.publish, publish_at=input.publish_at, is_promotion=input.is_promotion)
    if image is not None:
        update_data = replace(update_data, image=save_upload(image, ImageUpload.BLOG, obj.channel.ulid))

    category_data_ret = get_category_data(input.category_ulid)
    if category_data_ret.is_err:
        return Result.err(category_data_ret.err_value)

    category_data = category_data_ret.ok_value

    save_ret = atomic_result(lambda: save_blog_data(update_data, category_data, save_product))
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    if not obj.publish and input.publish:
        notification_ret = create_publish_notification_data(user_id, NotificationTypeNo.BLOG, obj.id, NotificationObjectType.BLOG)
        if notification_ret.is_err:
            return Result.err(notification_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_manage_blog(user_id: int, ulids: list[str]) -> Result[None, InputError]:
    repo = injector.get(BlogInterface)
    ids_ret = repo.get_ids(FilterOption(ulids=ulids, owner_id=user_id), SortOption(), PageOption(limit=len(ulids)))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    delete_ids = ids_ret.ok_value
    if len(delete_ids) != len(set(ulids)):
        log.warning("not found or owner mismatch", ulids=ulids, user_id=user_id)
        return Result.err(NotFoundError("error.deleteFailed"))

    purchase_ids_ret = get_product_purchase_ids_data(ProductType.BLOG, delete_ids)
    if purchase_ids_ret.is_err:
        return Result.err(purchase_ids_ret.err_value)

    purchase_ids = purchase_ids_ret.ok_value
    if len(purchase_ids) > 0:
        log.warning("purchased", ulids=ulids, user_id=user_id)
        return Result.err(ValidationError("error.deletePurchased"))

    delete_ret = atomic_result(lambda: delete_blog_data(delete_ids))
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def get_manage_comics(user_id: int, search: str, channel_ulid: str = "", limit: int = MEDIA_PAGE_SIZE, offset: int = 0) -> Result[tuple[list[ComicData], int], FatalError]:
    repo = injector.get(ComicInterface)
    filter = FilterOption(search=search, owner_id=user_id, channel_ulid=channel_ulid)
    count_ret = repo.count(filter)
    if count_ret.is_err:
        return Result.err(count_ret.err_value)

    total = count_ret.ok_value
    ids_ret = repo.get_ids(filter, SortOption(), PageOption(limit=limit, offset=offset))
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
def get_manage_comic(user_id: int, ulid: str) -> Result[tuple[ComicData, ProductData | None], FindError]:
    repo = injector.get(ComicInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid, owner_id=user_id), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.info("not found", ulid=ulid, user_id=user_id)
        return Result.err(NotFoundError("error.mediaNotFound"))

    objs_ret = repo.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]
    product_ret = get_product_data(ProductType.COMIC, obj.id)
    if product_ret.is_err:
        return Result.err(product_ret.err_value)

    product = product_ret.ok_value
    data = replace(obj, image=create_url(obj.image), pages=[create_url(p) for p in obj.pages])
    return Result.ok((data, product))


@Result.shield_exception()
def update_manage_comic(user_id: int, ulid: str, input: ComicUpdateDTO, image: UploadedFile | None = None) -> Result[None, WriteError]:
    upload_ret = validate_uploads([(image, ImageUpload.COMIC)])
    if upload_ret.is_err:
        return Result.err(upload_ret.err_value)

    repo = injector.get(ComicInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.warning("not found", ulid=ulid)
        return Result.err(NotFoundError("error.saveFailed"))

    objs_ret = repo.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]
    owner_id = obj.channel.owner_id
    if owner_id != user_id:
        log.error("owner mismatch", ulid=ulid, user_id=user_id, owner_id=owner_id)
        return Result.err(ForbiddenError("error.saveFailed"))

    product_ret = get_product_data(ProductType.COMIC, obj.id)
    if product_ret.is_err:
        return Result.err(product_ret.err_value)

    product = product_ret.ok_value
    if input.price == 0 and product is not None:
        purchase_ids_ret = get_purchase_ids_data([product.id])
        if purchase_ids_ret.is_err:
            return Result.err(purchase_ids_ret.err_value)

        purchase_ids = purchase_ids_ret.ok_value
        if len(purchase_ids) > 0:
            log.warning("purchased", ulid=ulid, user_id=user_id)
            return Result.err(ValidationError("error.saleStopPurchased"))

    save_product = product if input.price > 0 else None
    is_price_changed = product is None or input.price != product.price.amount
    if input.price > 0 and is_price_changed:
        currency_ret = get_seller_currency_data(user_id)
        if currency_ret.is_err:
            return Result.err(currency_ret.err_value)

        currency = currency_ret.ok_value
        save_product = ProductData(
            id=product.id if product is not None else 0,
            ulid=product.ulid if product is not None else "",
            seller_id=user_id,
            product_type=ProductType.COMIC,
            object_id=obj.id,
            price=Money(amount=input.price, currency=currency),
        )

    update_data = replace(obj, title=input.title, content=input.content, free_pages=input.free_pages, publish=input.publish, publish_at=input.publish_at)
    if image is not None:
        update_data = replace(update_data, image=save_upload(image, ImageUpload.COMIC, obj.channel.ulid))

    category_data_ret = get_category_data(input.category_ulid)
    if category_data_ret.is_err:
        return Result.err(category_data_ret.err_value)

    category_data = category_data_ret.ok_value

    save_ret = atomic_result(lambda: save_comic_data(update_data, category_data, save_product))
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    if not obj.publish and input.publish:
        notification_ret = create_publish_notification_data(user_id, NotificationTypeNo.COMIC, obj.id, NotificationObjectType.COMIC)
        if notification_ret.is_err:
            return Result.err(notification_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_manage_comic(user_id: int, ulids: list[str]) -> Result[None, InputError]:
    repo = injector.get(ComicInterface)
    ids_ret = repo.get_ids(FilterOption(ulids=ulids, owner_id=user_id), SortOption(), PageOption(limit=len(ulids)))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    delete_ids = ids_ret.ok_value
    if len(delete_ids) != len(set(ulids)):
        log.warning("not found or owner mismatch", ulids=ulids, user_id=user_id)
        return Result.err(NotFoundError("error.deleteFailed"))

    purchase_ids_ret = get_product_purchase_ids_data(ProductType.COMIC, delete_ids)
    if purchase_ids_ret.is_err:
        return Result.err(purchase_ids_ret.err_value)

    purchase_ids = purchase_ids_ret.ok_value
    if len(purchase_ids) > 0:
        log.warning("purchased", ulids=ulids, user_id=user_id)
        return Result.err(ValidationError("error.deletePurchased"))

    delete_ret = atomic_result(lambda: delete_comic_data(delete_ids))
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def get_manage_pictures(user_id: int, search: str, channel_ulid: str = "", limit: int = MEDIA_PAGE_SIZE, offset: int = 0) -> Result[tuple[list[PictureData], int], FatalError]:
    repo = injector.get(PictureInterface)
    filter = FilterOption(search=search, owner_id=user_id, channel_ulid=channel_ulid)
    count_ret = repo.count(filter)
    if count_ret.is_err:
        return Result.err(count_ret.err_value)

    total = count_ret.ok_value
    ids_ret = repo.get_ids(filter, SortOption(), PageOption(limit=limit, offset=offset))
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
def get_manage_picture(user_id: int, ulid: str) -> Result[PictureData, FindError]:
    repo = injector.get(PictureInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid, owner_id=user_id), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.info("not found", ulid=ulid, user_id=user_id)
        return Result.err(NotFoundError("error.mediaNotFound"))

    objs_ret = repo.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]
    return Result.ok(replace(obj, image=create_url(obj.image)))


@Result.shield_exception()
def update_manage_picture(user_id: int, ulid: str, input: PictureUpdateDTO, image: UploadedFile | None = None) -> Result[None, WriteError]:
    upload_ret = validate_uploads([(image, ImageUpload.PICTURE)])
    if upload_ret.is_err:
        return Result.err(upload_ret.err_value)

    repo = injector.get(PictureInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.warning("not found", ulid=ulid)
        return Result.err(NotFoundError("error.saveFailed"))

    objs_ret = repo.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]
    owner_id = obj.channel.owner_id
    if owner_id != user_id:
        log.error("owner mismatch", ulid=ulid, user_id=user_id, owner_id=owner_id)
        return Result.err(ForbiddenError("error.saveFailed"))

    update_data = replace(obj, title=input.title, content=input.content, publish=input.publish, publish_at=input.publish_at)
    if image is not None:
        update_data = replace(update_data, image=save_upload(image, ImageUpload.PICTURE, obj.channel.ulid))

    category_data_ret = get_category_data(input.category_ulid)
    if category_data_ret.is_err:
        return Result.err(category_data_ret.err_value)

    category_data = category_data_ret.ok_value

    save_ret = atomic_result(lambda: save_picture_data(update_data, category_data))
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    if not obj.publish and input.publish:
        notification_ret = create_publish_notification_data(user_id, NotificationTypeNo.PICTURE, obj.id, NotificationObjectType.PICTURE)
        if notification_ret.is_err:
            return Result.err(notification_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_manage_picture(user_id: int, ulids: list[str]) -> Result[None, FindError]:
    repo = injector.get(PictureInterface)
    ids_ret = repo.get_ids(FilterOption(ulids=ulids, owner_id=user_id), SortOption(), PageOption(limit=len(ulids)))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    delete_ids = ids_ret.ok_value
    if len(delete_ids) != len(set(ulids)):
        log.warning("not found or owner mismatch", ulids=ulids, user_id=user_id)
        return Result.err(NotFoundError("error.deleteFailed"))

    delete_ret = atomic_result(lambda: delete_picture_data(delete_ids))
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def get_manage_chats(user_id: int, search: str, channel_ulid: str = "", limit: int = MEDIA_PAGE_SIZE, offset: int = 0) -> Result[tuple[list[ChatData], int], FatalError]:
    repo = injector.get(ChatInterface)
    filter = FilterOption(search=search, owner_id=user_id, channel_ulid=channel_ulid)
    count_ret = repo.count(filter)
    if count_ret.is_err:
        return Result.err(count_ret.err_value)

    total = count_ret.ok_value
    ids_ret = repo.get_ids(filter, SortOption(), PageOption(limit=limit, offset=offset))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    objs_ret = repo.bulk_get(ids=ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    return Result.ok((objs, total))


@Result.shield_exception()
def get_manage_chat(user_id: int, ulid: str) -> Result[ChatData, FindError]:
    repo = injector.get(ChatInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid, owner_id=user_id), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.info("not found", ulid=ulid, user_id=user_id)
        return Result.err(NotFoundError("error.mediaNotFound"))

    objs_ret = repo.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    return Result.ok(objs[0])


@Result.shield_exception()
def update_manage_chat(user_id: int, ulid: str, input: ChatUpdateDTO) -> Result[None, WriteError]:
    repo = injector.get(ChatInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.warning("not found", ulid=ulid)
        return Result.err(NotFoundError("error.saveFailed"))

    objs_ret = repo.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]
    owner_id = obj.channel.owner_id
    if owner_id != user_id:
        log.error("owner mismatch", ulid=ulid, user_id=user_id, owner_id=owner_id)
        return Result.err(ForbiddenError("error.saveFailed"))

    if timezone.localdate(input.publish_at) > input.period:
        return Result.err(ValidationError("error.publishAtAfterPeriod"))

    update_data = replace(obj, title=input.title, content=input.content, period=input.period, publish=input.publish, publish_at=input.publish_at)
    category_data_ret = get_category_data(input.category_ulid)
    if category_data_ret.is_err:
        return Result.err(category_data_ret.err_value)

    category_data = category_data_ret.ok_value

    save_ret = atomic_result(lambda: save_chat_data(update_data, category_data))
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    if not obj.publish and input.publish:
        notification_ret = create_publish_notification_data(user_id, NotificationTypeNo.CHAT, obj.id, NotificationObjectType.CHAT)
        if notification_ret.is_err:
            return Result.err(notification_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_manage_chat(user_id: int, ulids: list[str]) -> Result[None, FindError]:
    repo = injector.get(ChatInterface)
    ids_ret = repo.get_ids(FilterOption(ulids=ulids, owner_id=user_id), SortOption(), PageOption(limit=len(ulids)))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    delete_ids = ids_ret.ok_value
    if len(delete_ids) != len(set(ulids)):
        log.warning("not found or owner mismatch", ulids=ulids, user_id=user_id)
        return Result.err(NotFoundError("error.deleteFailed"))

    message_repo = injector.get(MessageInterface)
    reply_ids_ret = message_repo.get_ids(MessageFilterOption(chat_ids=delete_ids, is_parent=False), MessageSortOption(), MessagePageOption())
    if reply_ids_ret.is_err:
        return Result.err(reply_ids_ret.err_value)

    reply_ids = reply_ids_ret.ok_value
    delete_ret = atomic_result(lambda: delete_chat_data(delete_ids, reply_ids))
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    return Result.ok(None)
