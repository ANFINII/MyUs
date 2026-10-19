from dataclasses import replace
from datetime import date
from django.db import transaction
from ninja import UploadedFile
from api.modules.logger import log
from api.src.domain.interface.category.data import CategoryData
from api.src.domain.interface.category.interface import CategoryInterface
from api.src.domain.interface.media.video.data import VideoData
from api.src.domain.interface.media.video.interface import VideoInterface
from api.src.domain.interface.media.music.data import MusicData
from api.src.domain.interface.media.music.interface import MusicInterface
from api.src.domain.interface.media.blog.data import BlogData
from api.src.domain.interface.media.blog.interface import BlogInterface
from api.src.domain.interface.media.comic.data import ComicData
from api.src.domain.interface.media.comic.interface import ComicInterface
from api.src.domain.interface.media.picture.data import PictureData
from api.src.domain.interface.media.picture.interface import PictureInterface
from api.src.domain.interface.media.chat.data import ChatData
from api.src.domain.interface.media.chat.interface import ChatInterface
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, PAGE_SIZE, PageOption, SortOption
from api.src.domain.interface.message.interface import FilterOption as MessageFilterOption, MessageInterface, SortOption as MessageSortOption
from api.src.injectors.container import injector
from api.src.types.schema.media.input import VideoUpdateIn, MusicUpdateIn, BlogUpdateIn, ComicUpdateIn, PictureUpdateIn, ChatUpdateIn
from api.src.usecase.notification import create_publish_notification, delete_object_notifications
from api.utils.common.result import FatalError, NotFoundError, Result
from api.utils.enum.media import MediaType
from api.utils.enum.notification import NotificationObjectType, NotificationTypeNo
from api.utils.enum.upload import ImageUpload
from api.utils.functions.index import create_url
from api.utils.functions.media import save_upload


@Result.shield_exception()
def get_manage_videos(user_id: int, search: str, channel_ulid: str = "", limit: int = PAGE_SIZE, offset: int = 0) -> Result[tuple[list[VideoData], int], FatalError]:
    repository = injector.get(VideoInterface)
    filter = FilterOption(search=search, owner_id=user_id, channel_ulid=channel_ulid)
    count_ret = repository.count(filter)
    if count_ret.is_err:
        return Result.err(count_ret.err_value)

    total = count_ret.ok_value
    ids_ret = repository.get_ids(filter, ExcludeOption(), SortOption(), PageOption(limit=limit, offset=offset))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    objs_ret = repository.bulk_get(ids=ids_ret.ok_value)
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
def get_manage_video(user_id: int, ulid: str) -> Result[VideoData, NotFoundError | FatalError]:
    repository = injector.get(VideoInterface)
    ids_ret = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.info("data not found", ulid=ulid, user_id=user_id)
        return Result.err(NotFoundError("data not found"))

    objs_ret = repository.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    obj = objs_ret.ok_value[0]
    return Result.ok(replace(obj,
        image=create_url(obj.image),
        video=create_url(obj.video),
        convert=create_url(obj.convert),
    ))


@Result.shield_exception()
def update_manage_video(user_id: int, ulid: str, input: VideoUpdateIn, image: UploadedFile | None = None) -> Result[None, NotFoundError | FatalError]:
    repository = injector.get(VideoInterface)
    ids_ret = repository.get_ids(FilterOption(ulid=ulid), ExcludeOption(), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.error("Video not found", ulid=ulid)
        return Result.err(NotFoundError("保存に失敗しました!"))

    objs_ret = repository.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    obj = objs_ret.ok_value[0]
    if obj.channel.owner_id != user_id:
        log.error("Video owner mismatch", ulid=ulid, user_id=user_id, owner_id=obj.channel.owner_id)
        return Result.err(NotFoundError("保存に失敗しました!"))

    update_data = replace(obj, title=input.title, content=input.content, publish=input.publish)
    if image is not None:
        update_data = replace(update_data, image=save_upload(image, ImageUpload.VIDEO, obj.channel.ulid))

    category_repo = injector.get(CategoryInterface)
    categories = [CategoryData(id=0, ulid=input.category_ulid, jp_name="", en_name="")] if input.category_ulid else []

    with transaction.atomic():
        save_ret = repository.bulk_save([update_data])
        if save_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(save_ret.err_value)

        category_ret = category_repo.bulk_save(MediaType.VIDEO, obj.id, categories)
        if category_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(category_ret.err_value)

    if not obj.publish and input.publish and obj.convert != "":
        notification_ret = create_publish_notification(user_id, NotificationTypeNo.VIDEO, obj.id, NotificationObjectType.VIDEO)
        if notification_ret.is_err:
            return Result.err(notification_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_manage_video(user_id: int, ulids: list[str]) -> Result[None, NotFoundError | FatalError]:
    repository = injector.get(VideoInterface)
    delete_ids: list[int] = []

    for ulid in ulids:
        ids_ret = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption(), PageOption())
        if ids_ret.is_err:
            return Result.err(ids_ret.err_value)

        ids = ids_ret.ok_value
        if len(ids) == 0:
            log.error("Video not found or owner mismatch", ulid=ulid, user_id=user_id)
            return Result.err(NotFoundError("削除に失敗しました!"))
        delete_ids.append(ids[0])

    with transaction.atomic():
        delete_ret = repository.bulk_delete(delete_ids)
        if delete_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(delete_ret.err_value)

        notification_ret = delete_object_notifications(NotificationObjectType.VIDEO, delete_ids)
        if notification_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(notification_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def get_manage_musics(user_id: int, search: str, channel_ulid: str = "", limit: int = PAGE_SIZE, offset: int = 0) -> Result[tuple[list[MusicData], int], FatalError]:
    repository = injector.get(MusicInterface)
    filter = FilterOption(search=search, owner_id=user_id, channel_ulid=channel_ulid)
    count_ret = repository.count(filter)
    if count_ret.is_err:
        return Result.err(count_ret.err_value)

    total = count_ret.ok_value
    ids_ret = repository.get_ids(filter, ExcludeOption(), SortOption(), PageOption(limit=limit, offset=offset))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    objs_ret = repository.bulk_get(ids=ids_ret.ok_value)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value

    data = [replace(o, music=create_url(o.music)) for o in objs]
    return Result.ok((data, total))


@Result.shield_exception()
def get_manage_music(user_id: int, ulid: str) -> Result[MusicData, NotFoundError | FatalError]:
    repository = injector.get(MusicInterface)
    ids_ret = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.info("data not found", ulid=ulid, user_id=user_id)
        return Result.err(NotFoundError("data not found"))

    objs_ret = repository.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    obj = objs_ret.ok_value[0]
    return Result.ok(replace(obj, music=create_url(obj.music)))


@Result.shield_exception()
def update_manage_music(user_id: int, ulid: str, input: MusicUpdateIn) -> Result[None, NotFoundError | FatalError]:
    repository = injector.get(MusicInterface)
    ids_ret = repository.get_ids(FilterOption(ulid=ulid), ExcludeOption(), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.error("Music not found", ulid=ulid)
        return Result.err(NotFoundError("保存に失敗しました!"))

    objs_ret = repository.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    obj = objs_ret.ok_value[0]
    if obj.channel.owner_id != user_id:
        log.error("Music owner mismatch", ulid=ulid, user_id=user_id, owner_id=obj.channel.owner_id)
        return Result.err(NotFoundError("保存に失敗しました!"))

    update_data = replace(obj, title=input.title, content=input.content, lyric=input.lyric, download=input.download, publish=input.publish)
    category_repo = injector.get(CategoryInterface)
    categories = [CategoryData(id=0, ulid=input.category_ulid, jp_name="", en_name="")] if input.category_ulid else []

    with transaction.atomic():
        save_ret = repository.bulk_save([update_data])
        if save_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(save_ret.err_value)

        category_ret = category_repo.bulk_save(MediaType.MUSIC, obj.id, categories)
        if category_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(category_ret.err_value)

    if not obj.publish and input.publish:
        notification_ret = create_publish_notification(user_id, NotificationTypeNo.MUSIC, obj.id, NotificationObjectType.MUSIC)
        if notification_ret.is_err:
            return Result.err(notification_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_manage_music(user_id: int, ulids: list[str]) -> Result[None, NotFoundError | FatalError]:
    repository = injector.get(MusicInterface)
    delete_ids: list[int] = []

    for ulid in ulids:
        ids_ret = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption(), PageOption())
        if ids_ret.is_err:
            return Result.err(ids_ret.err_value)

        ids = ids_ret.ok_value
        if len(ids) == 0:
            log.error("Music not found or owner mismatch", ulid=ulid, user_id=user_id)
            return Result.err(NotFoundError("削除に失敗しました!"))
        delete_ids.append(ids[0])

    with transaction.atomic():
        delete_ret = repository.bulk_delete(delete_ids)
        if delete_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(delete_ret.err_value)

        notification_ret = delete_object_notifications(NotificationObjectType.MUSIC, delete_ids)
        if notification_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(notification_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def get_manage_blogs(user_id: int, search: str, channel_ulid: str = "", limit: int = PAGE_SIZE, offset: int = 0) -> Result[tuple[list[BlogData], int], FatalError]:
    repository = injector.get(BlogInterface)
    filter = FilterOption(search=search, owner_id=user_id, channel_ulid=channel_ulid)
    count_ret = repository.count(filter)
    if count_ret.is_err:
        return Result.err(count_ret.err_value)

    total = count_ret.ok_value
    ids_ret = repository.get_ids(filter, ExcludeOption(), SortOption(), PageOption(limit=limit, offset=offset))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    objs_ret = repository.bulk_get(ids=ids_ret.ok_value)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value

    data = [replace(o, image=create_url(o.image)) for o in objs]
    return Result.ok((data, total))


@Result.shield_exception()
def get_manage_blog(user_id: int, ulid: str) -> Result[BlogData, NotFoundError | FatalError]:
    repository = injector.get(BlogInterface)
    ids_ret = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.info("data not found", ulid=ulid, user_id=user_id)
        return Result.err(NotFoundError("data not found"))

    objs_ret = repository.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    obj = objs_ret.ok_value[0]
    return Result.ok(replace(obj, image=create_url(obj.image)))


@Result.shield_exception()
def update_manage_blog(user_id: int, ulid: str, input: BlogUpdateIn, image: UploadedFile | None = None) -> Result[None, NotFoundError | FatalError]:
    repository = injector.get(BlogInterface)
    ids_ret = repository.get_ids(FilterOption(ulid=ulid), ExcludeOption(), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.error("Blog not found", ulid=ulid)
        return Result.err(NotFoundError("保存に失敗しました!"))

    objs_ret = repository.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    obj = objs_ret.ok_value[0]
    if obj.channel.owner_id != user_id:
        log.error("Blog owner mismatch", ulid=ulid, user_id=user_id, owner_id=obj.channel.owner_id)
        return Result.err(NotFoundError("保存に失敗しました!"))

    update_data = replace(obj, title=input.title, content=input.content, richtext=input.richtext, publish=input.publish)
    if image is not None:
        update_data = replace(update_data, image=save_upload(image, ImageUpload.BLOG, obj.channel.ulid))

    category_repo = injector.get(CategoryInterface)
    categories = [CategoryData(id=0, ulid=input.category_ulid, jp_name="", en_name="")] if input.category_ulid else []

    with transaction.atomic():
        save_ret = repository.bulk_save([update_data])
        if save_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(save_ret.err_value)

        category_ret = category_repo.bulk_save(MediaType.BLOG, obj.id, categories)
        if category_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(category_ret.err_value)

    if not obj.publish and input.publish:
        notification_ret = create_publish_notification(user_id, NotificationTypeNo.BLOG, obj.id, NotificationObjectType.BLOG)
        if notification_ret.is_err:
            return Result.err(notification_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_manage_blog(user_id: int, ulids: list[str]) -> Result[None, NotFoundError | FatalError]:
    repository = injector.get(BlogInterface)
    delete_ids: list[int] = []

    for ulid in ulids:
        ids_ret = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption(), PageOption())
        if ids_ret.is_err:
            return Result.err(ids_ret.err_value)

        ids = ids_ret.ok_value
        if len(ids) == 0:
            log.error("Blog not found or owner mismatch", ulid=ulid, user_id=user_id)
            return Result.err(NotFoundError("削除に失敗しました!"))
        delete_ids.append(ids[0])

    with transaction.atomic():
        delete_ret = repository.bulk_delete(delete_ids)
        if delete_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(delete_ret.err_value)

        notification_ret = delete_object_notifications(NotificationObjectType.BLOG, delete_ids)
        if notification_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(notification_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def get_manage_comics(user_id: int, search: str, channel_ulid: str = "", limit: int = PAGE_SIZE, offset: int = 0) -> Result[tuple[list[ComicData], int], FatalError]:
    repository = injector.get(ComicInterface)
    filter = FilterOption(search=search, owner_id=user_id, channel_ulid=channel_ulid)
    count_ret = repository.count(filter)
    if count_ret.is_err:
        return Result.err(count_ret.err_value)

    total = count_ret.ok_value
    ids_ret = repository.get_ids(filter, ExcludeOption(), SortOption(), PageOption(limit=limit, offset=offset))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    objs_ret = repository.bulk_get(ids=ids_ret.ok_value)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value

    data = [replace(o,
        image=create_url(o.image),
        pages=[create_url(p) for p in o.pages],
    ) for o in objs]
    return Result.ok((data, total))


@Result.shield_exception()
def get_manage_comic(user_id: int, ulid: str) -> Result[ComicData, NotFoundError | FatalError]:
    repository = injector.get(ComicInterface)
    ids_ret = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.info("data not found", ulid=ulid, user_id=user_id)
        return Result.err(NotFoundError("data not found"))

    objs_ret = repository.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    obj = objs_ret.ok_value[0]
    return Result.ok(replace(obj,
        image=create_url(obj.image),
        pages=[create_url(p) for p in obj.pages],
    ))


@Result.shield_exception()
def update_manage_comic(user_id: int, ulid: str, input: ComicUpdateIn, image: UploadedFile | None = None) -> Result[None, NotFoundError | FatalError]:
    repository = injector.get(ComicInterface)
    ids_ret = repository.get_ids(FilterOption(ulid=ulid), ExcludeOption(), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.error("Comic not found", ulid=ulid)
        return Result.err(NotFoundError("保存に失敗しました!"))

    objs_ret = repository.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    obj = objs_ret.ok_value[0]
    if obj.channel.owner_id != user_id:
        log.error("Comic owner mismatch", ulid=ulid, user_id=user_id, owner_id=obj.channel.owner_id)
        return Result.err(NotFoundError("保存に失敗しました!"))

    update_data = replace(obj, title=input.title, content=input.content, publish=input.publish)
    if image is not None:
        update_data = replace(update_data, image=save_upload(image, ImageUpload.COMIC, obj.channel.ulid))

    category_repo = injector.get(CategoryInterface)
    categories = [CategoryData(id=0, ulid=input.category_ulid, jp_name="", en_name="")] if input.category_ulid else []

    with transaction.atomic():
        save_ret = repository.bulk_save([update_data])
        if save_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(save_ret.err_value)

        category_ret = category_repo.bulk_save(MediaType.COMIC, obj.id, categories)
        if category_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(category_ret.err_value)

    if not obj.publish and input.publish:
        notification_ret = create_publish_notification(user_id, NotificationTypeNo.COMIC, obj.id, NotificationObjectType.COMIC)
        if notification_ret.is_err:
            return Result.err(notification_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_manage_comic(user_id: int, ulids: list[str]) -> Result[None, NotFoundError | FatalError]:
    repository = injector.get(ComicInterface)
    delete_ids: list[int] = []

    for ulid in ulids:
        ids_ret = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption(), PageOption())
        if ids_ret.is_err:
            return Result.err(ids_ret.err_value)

        ids = ids_ret.ok_value
        if len(ids) == 0:
            log.error("Comic not found or owner mismatch", ulid=ulid, user_id=user_id)
            return Result.err(NotFoundError("削除に失敗しました!"))
        delete_ids.append(ids[0])

    with transaction.atomic():
        delete_ret = repository.bulk_delete(delete_ids)
        if delete_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(delete_ret.err_value)

        notification_ret = delete_object_notifications(NotificationObjectType.COMIC, delete_ids)
        if notification_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(notification_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def get_manage_pictures(user_id: int, search: str, channel_ulid: str = "", limit: int = PAGE_SIZE, offset: int = 0) -> Result[tuple[list[PictureData], int], FatalError]:
    repository = injector.get(PictureInterface)
    filter = FilterOption(search=search, owner_id=user_id, channel_ulid=channel_ulid)
    count_ret = repository.count(filter)
    if count_ret.is_err:
        return Result.err(count_ret.err_value)

    total = count_ret.ok_value
    ids_ret = repository.get_ids(filter, ExcludeOption(), SortOption(), PageOption(limit=limit, offset=offset))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    objs_ret = repository.bulk_get(ids=ids_ret.ok_value)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value

    data = [replace(o, image=create_url(o.image)) for o in objs]
    return Result.ok((data, total))


@Result.shield_exception()
def get_manage_picture(user_id: int, ulid: str) -> Result[PictureData, NotFoundError | FatalError]:
    repository = injector.get(PictureInterface)
    ids_ret = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.info("data not found", ulid=ulid, user_id=user_id)
        return Result.err(NotFoundError("data not found"))

    objs_ret = repository.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    obj = objs_ret.ok_value[0]
    return Result.ok(replace(obj, image=create_url(obj.image)))


@Result.shield_exception()
def update_manage_picture(user_id: int, ulid: str, input: PictureUpdateIn, image: UploadedFile | None = None) -> Result[None, NotFoundError | FatalError]:
    repository = injector.get(PictureInterface)
    ids_ret = repository.get_ids(FilterOption(ulid=ulid), ExcludeOption(), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.error("Picture not found", ulid=ulid)
        return Result.err(NotFoundError("保存に失敗しました!"))

    objs_ret = repository.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    obj = objs_ret.ok_value[0]
    if obj.channel.owner_id != user_id:
        log.error("Picture owner mismatch", ulid=ulid, user_id=user_id, owner_id=obj.channel.owner_id)
        return Result.err(NotFoundError("保存に失敗しました!"))

    update_data = replace(obj, title=input.title, content=input.content, publish=input.publish)
    if image is not None:
        update_data = replace(update_data, image=save_upload(image, ImageUpload.PICTURE, obj.channel.ulid))

    category_repo = injector.get(CategoryInterface)
    categories = [CategoryData(id=0, ulid=input.category_ulid, jp_name="", en_name="")] if input.category_ulid else []

    with transaction.atomic():
        save_ret = repository.bulk_save([update_data])
        if save_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(save_ret.err_value)

        category_ret = category_repo.bulk_save(MediaType.PICTURE, obj.id, categories)
        if category_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(category_ret.err_value)

    if not obj.publish and input.publish:
        notification_ret = create_publish_notification(user_id, NotificationTypeNo.PICTURE, obj.id, NotificationObjectType.PICTURE)
        if notification_ret.is_err:
            return Result.err(notification_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_manage_picture(user_id: int, ulids: list[str]) -> Result[None, NotFoundError | FatalError]:
    repository = injector.get(PictureInterface)
    delete_ids: list[int] = []

    for ulid in ulids:
        ids_ret = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption(), PageOption())
        if ids_ret.is_err:
            return Result.err(ids_ret.err_value)

        ids = ids_ret.ok_value
        if len(ids) == 0:
            log.error("Picture not found or owner mismatch", ulid=ulid, user_id=user_id)
            return Result.err(NotFoundError("削除に失敗しました!"))
        delete_ids.append(ids[0])

    with transaction.atomic():
        delete_ret = repository.bulk_delete(delete_ids)
        if delete_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(delete_ret.err_value)

        notification_ret = delete_object_notifications(NotificationObjectType.PICTURE, delete_ids)
        if notification_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(notification_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def get_manage_chats(user_id: int, search: str, channel_ulid: str = "", limit: int = PAGE_SIZE, offset: int = 0) -> Result[tuple[list[ChatData], int], FatalError]:
    repository = injector.get(ChatInterface)
    filter = FilterOption(search=search, owner_id=user_id, channel_ulid=channel_ulid)
    count_ret = repository.count(filter)
    if count_ret.is_err:
        return Result.err(count_ret.err_value)

    total = count_ret.ok_value
    ids_ret = repository.get_ids(filter, ExcludeOption(), SortOption(), PageOption(limit=limit, offset=offset))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    objs_ret = repository.bulk_get(ids=ids_ret.ok_value)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    return Result.ok((objs, total))


@Result.shield_exception()
def get_manage_chat(user_id: int, ulid: str) -> Result[ChatData, NotFoundError | FatalError]:
    repository = injector.get(ChatInterface)
    ids_ret = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.info("data not found", ulid=ulid, user_id=user_id)
        return Result.err(NotFoundError("data not found"))

    objs_ret = repository.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    return Result.ok(objs_ret.ok_value[0])


@Result.shield_exception()
def update_manage_chat(user_id: int, ulid: str, input: ChatUpdateIn) -> Result[None, NotFoundError | FatalError]:
    repository = injector.get(ChatInterface)
    ids_ret = repository.get_ids(FilterOption(ulid=ulid), ExcludeOption(), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.error("Chat not found", ulid=ulid)
        return Result.err(NotFoundError("保存に失敗しました!"))

    objs_ret = repository.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    obj = objs_ret.ok_value[0]
    if obj.channel.owner_id != user_id:
        log.error("Chat owner mismatch", ulid=ulid, user_id=user_id, owner_id=obj.channel.owner_id)
        return Result.err(NotFoundError("保存に失敗しました!"))

    update_data = replace(obj, title=input.title, content=input.content, period=date.fromisoformat(input.period), publish=input.publish)
    category_repo = injector.get(CategoryInterface)
    categories = [CategoryData(id=0, ulid=input.category_ulid, jp_name="", en_name="")] if input.category_ulid else []

    with transaction.atomic():
        save_ret = repository.bulk_save([update_data])
        if save_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(save_ret.err_value)

        category_ret = category_repo.bulk_save(MediaType.CHAT, obj.id, categories)
        if category_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(category_ret.err_value)

    if not obj.publish and input.publish:
        notification_ret = create_publish_notification(user_id, NotificationTypeNo.CHAT, obj.id, NotificationObjectType.CHAT)
        if notification_ret.is_err:
            return Result.err(notification_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_manage_chat(user_id: int, ulids: list[str]) -> Result[None, NotFoundError | FatalError]:
    repository = injector.get(ChatInterface)
    delete_ids: list[int] = []

    for ulid in ulids:
        ids_ret = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption(), PageOption())
        if ids_ret.is_err:
            return Result.err(ids_ret.err_value)

        ids = ids_ret.ok_value
        if len(ids) == 0:
            log.error("Chat not found or owner mismatch", ulid=ulid, user_id=user_id)
            return Result.err(NotFoundError("削除に失敗しました!"))
        delete_ids.append(ids[0])

    message_repo = injector.get(MessageInterface)
    reply_ids: list[int] = []
    for chat_id in delete_ids:
        reply_ids_ret = message_repo.get_ids(MessageFilterOption(chat_id=chat_id, is_parent=False), MessageSortOption())
        if reply_ids_ret.is_err:
            return Result.err(reply_ids_ret.err_value)
        reply_ids += reply_ids_ret.ok_value

    with transaction.atomic():
        delete_ret = repository.bulk_delete(delete_ids)
        if delete_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(delete_ret.err_value)

        chat_notification_ret = delete_object_notifications(NotificationObjectType.CHAT, delete_ids)
        if chat_notification_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(chat_notification_ret.err_value)

        message_notification_ret = delete_object_notifications(NotificationObjectType.MESSAGE, reply_ids)
        if message_notification_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(message_notification_ret.err_value)

    return Result.ok(None)
