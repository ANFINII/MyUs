from dataclasses import replace
from ninja import UploadedFile
from api.modules.logger import log
from api.src.domain.interface.media.blog.data import BlogData
from api.src.domain.interface.media.blog.interface import BlogInterface
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, PAGE_SIZE, PageOption, SortOption
from api.src.injectors.container import injector
from api.src.types.schema.media.input import BlogUpdateIn
from api.src.usecase.category import get_category_data
from api.src.usecase.notification import create_publish_notification
from api.src.usecase.manage.media._data import save_blog_data, delete_blog_data
from api.utils.common.result import FatalError, FindError, ForbiddenError, NotFoundError, Result, ValidationError, WriteError
from api.utils.enum.notification import NotificationObjectType, NotificationTypeNo
from api.utils.enum.upload import ImageUpload
from api.utils.functions.index import create_url
from api.utils.functions.media import save_upload, validate_uploads
from api.utils.functions.transaction import atomic_result


@Result.shield_exception()
def get_manage_blogs(user_id: int, search: str, channel_ulid: str = "", limit: int = PAGE_SIZE, offset: int = 0) -> Result[tuple[list[BlogData], int], FatalError]:
    repo = injector.get(BlogInterface)
    filter = FilterOption(search=search, owner_id=user_id, channel_ulid=channel_ulid)
    count_ret = repo.count(filter)
    if count_ret.is_err:
        return Result.err(count_ret.err_value)

    total = count_ret.ok_value
    ids_ret = repo.get_ids(filter, ExcludeOption(), SortOption(), PageOption(limit=limit, offset=offset))
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
def get_manage_blog(user_id: int, ulid: str) -> Result[BlogData, FindError]:
    repo = injector.get(BlogInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.info("data not found", ulid=ulid, user_id=user_id)
        return Result.err(NotFoundError("data not found"))

    objs_ret = repo.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]
    return Result.ok(replace(obj, image=create_url(obj.image)))


@Result.shield_exception()
def update_manage_blog(user_id: int, ulid: str, input: BlogUpdateIn, image: UploadedFile | None = None) -> Result[None, WriteError]:
    upload_ret = validate_uploads([(image, ImageUpload.BLOG)])
    if upload_ret.is_err:
        return Result.err(upload_ret.err_value)

    repo = injector.get(BlogInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid), ExcludeOption(), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.error("Blog not found", ulid=ulid)
        return Result.err(NotFoundError("error.saveFailed"))

    objs_ret = repo.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]
    if obj.channel.owner_id != user_id:
        log.error("Blog owner mismatch", ulid=ulid, user_id=user_id, owner_id=obj.channel.owner_id)
        return Result.err(ForbiddenError("error.saveFailed"))

    update_data = replace(obj, title=input.title, content=input.content, richtext=input.richtext, publish=input.publish, publish_at=input.publish_at, is_promotion=input.is_promotion)
    if image is not None:
        update_data = replace(update_data, image=save_upload(image, ImageUpload.BLOG, obj.channel.ulid))

    category_data_ret = get_category_data(input.category_ulid)
    if category_data_ret.is_err:
        return Result.err(category_data_ret.err_value)

    category_data = category_data_ret.ok_value
    if category_data is None:
        return Result.err(ValidationError("error.categoryRequired"))

    save_ret = atomic_result(lambda: save_blog_data(update_data, category_data))
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    if not obj.publish and input.publish:
        notification_ret = create_publish_notification(user_id, NotificationTypeNo.BLOG, obj.id, NotificationObjectType.BLOG)
        if notification_ret.is_err:
            return Result.err(notification_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_manage_blog(user_id: int, ulids: list[str]) -> Result[None, FindError]:
    repo = injector.get(BlogInterface)
    ids_ret = repo.get_ids(FilterOption(ulids=ulids, owner_id=user_id), ExcludeOption(), SortOption(), PageOption(limit=len(ulids)))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    delete_ids = ids_ret.ok_value
    if len(delete_ids) != len(set(ulids)):
        log.error("Blog not found or owner mismatch", ulids=ulids, user_id=user_id)
        return Result.err(NotFoundError("error.deleteFailed"))

    delete_ret = atomic_result(lambda: delete_blog_data(delete_ids))
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    return Result.ok(None)
