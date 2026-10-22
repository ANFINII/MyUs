from dataclasses import replace
from datetime import datetime
from django.db import transaction
from ninja import UploadedFile
from api.modules.logger import log
from api.src.domain.interface.advertise.data import AdvertiseData
from api.src.domain.interface.advertise.interface import AdvertiseInterface
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, PAGE_SIZE, PageOption, SortOption
from api.src.injectors.container import injector
from api.src.types.schema.advertise import AdvertiseIn, AdvertiseUpdateIn
from api.src.usecase.user import get_user_data
from api.utils.common.result import FatalError, FindError, InputError, NotFoundError, Result, ValidationError
from api.utils.enum.upload import ImageUpload, MediaUpload
from api.utils.functions.index import create_url
from api.utils.functions.media import save_upload, validate_uploads
from api.utils.functions.validation import has_url


ADVERTISE_TYPE_PERSONAL = "one"
ADVERTISE_PERSONAL_LIMIT = 5


@Result.shield_exception()
def get_manage_advertises(user_id: int, search: str, limit: int = PAGE_SIZE, offset: int = 0) -> Result[tuple[list[AdvertiseData], int], FatalError]:
    repo = injector.get(AdvertiseInterface)
    filter = FilterOption(search=search, owner_id=user_id)
    total_ret = repo.count(filter)
    if total_ret.is_err:
        return Result.err(total_ret.err_value)

    total = total_ret.ok_value
    ids_ret = repo.get_ids(filter, ExcludeOption(), SortOption(), PageOption(limit=limit, offset=offset))
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
    ) for o in objs]

    return Result.ok((data, total))


@Result.shield_exception()
def get_manage_advertise(user_id: int, ulid: str) -> Result[AdvertiseData, FindError]:
    repo = injector.get(AdvertiseInterface)
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
    return Result.ok(replace(obj,
        image=create_url(obj.image),
        video=create_url(obj.video),
    ))


@Result.shield_exception()
def create_manage_advertise(user_id: int, input: AdvertiseIn, image: UploadedFile, video: UploadedFile | None) -> Result[AdvertiseData, InputError]:
    if has_url(input.url):
        return Result.err(ValidationError("error.urlInvalid"))

    upload_ret = validate_uploads([(image, ImageUpload.ADVERTISE), (video, MediaUpload.ADVERTISE)])
    if upload_ret.is_err:
        return Result.err(upload_ret.err_value)

    repo = injector.get(AdvertiseInterface)

    count_ret = repo.count(FilterOption(owner_id=user_id))
    if count_ret.is_err:
        return Result.err(count_ret.err_value)

    count = count_ret.ok_value
    if count >= ADVERTISE_PERSONAL_LIMIT:
        log.error("Advertise limit exceeded", user_id=user_id, count=count)
        return Result.err(ValidationError("error.createFailed"))

    user_ret = get_user_data(user_id=user_id)
    if user_ret.is_err:
        return Result.err(user_ret.err_value)

    user = user_ret.ok_value
    if user is None:
        log.error("User not found", user_id=user_id)
        return Result.err(NotFoundError("error.createFailed"))

    new_advertise = AdvertiseData(
        id=0,
        ulid="",
        author_id=user_id,
        title=input.title,
        url=input.url,
        content=input.content,
        image=save_upload(image, ImageUpload.ADVERTISE, user.user.ulid),
        video=save_upload(video, MediaUpload.ADVERTISE, user.user.ulid) if video is not None else "",
        read=0,
        type=ADVERTISE_TYPE_PERSONAL,
        period=input.period,
        publish=input.publish,
        created=datetime.min,
        updated=datetime.min,
    )

    with transaction.atomic():
        new_ids_ret = repo.bulk_save([new_advertise])
        if new_ids_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(new_ids_ret.err_value)

        new_ids = new_ids_ret.ok_value
        assert len(new_ids) == 1, "作成に失敗しました"

    objs_ret = repo.bulk_get(new_ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    return Result.ok(objs[0])


@Result.shield_exception()
def update_manage_advertise(user_id: int, ulid: str, input: AdvertiseUpdateIn, image: UploadedFile | None, video: UploadedFile | None) -> Result[None, InputError]:
    if has_url(input.url):
        return Result.err(ValidationError("error.urlInvalid"))

    upload_ret = validate_uploads([(image, ImageUpload.ADVERTISE), (video, MediaUpload.ADVERTISE)])
    if upload_ret.is_err:
        return Result.err(upload_ret.err_value)

    repo = injector.get(AdvertiseInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.error("Advertise not found", ulid=ulid, user_id=user_id)
        return Result.err(NotFoundError("error.saveFailed"))

    objs_ret = repo.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]

    user_ret = get_user_data(user_id=user_id)
    if user_ret.is_err:
        return Result.err(user_ret.err_value)

    user = user_ret.ok_value
    if user is None:
        log.error("User not found", user_id=user_id)
        return Result.err(NotFoundError("error.saveFailed"))

    update_data = replace(obj,
        title=input.title,
        url=input.url,
        content=input.content,
        period=input.period,
        publish=input.publish,
    )
    if image is not None:
        update_data = replace(update_data, image=save_upload(image, ImageUpload.ADVERTISE, user.user.ulid))
    if video is not None:
        update_data = replace(update_data, video=save_upload(video, MediaUpload.ADVERTISE, user.user.ulid))

    with transaction.atomic():
        save_ret = repo.bulk_save([update_data])
        if save_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(save_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_manage_advertise(user_id: int, ulids: list[str]) -> Result[None, FindError]:
    repo = injector.get(AdvertiseInterface)
    ids_ret = repo.get_ids(FilterOption(ulids=ulids, owner_id=user_id), ExcludeOption(), SortOption(), PageOption(limit=len(ulids)))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) != len(set(ulids)):
        log.error("Advertise not found", ulids=ulids, user_id=user_id)
        return Result.err(NotFoundError("error.deleteFailed"))

    delete_ret = repo.bulk_delete(ids)
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    return Result.ok(None)
