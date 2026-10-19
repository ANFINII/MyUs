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
from api.utils.common.result import FatalError, NotFoundError, Result
from api.utils.enum.upload import ImageUpload, MediaUpload
from api.utils.functions.index import create_url
from api.utils.functions.media import save_upload


ADVERTISE_TYPE_PERSONAL = "one"
ADVERTISE_PERSONAL_LIMIT = 5


@Result.shield_exception()
def get_manage_advertises(user_id: int, search: str, limit: int = PAGE_SIZE, offset: int = 0) -> Result[tuple[list[AdvertiseData], int], FatalError]:
    repository = injector.get(AdvertiseInterface)
    filter = FilterOption(search=search, owner_id=user_id)
    total_ret = repository.count(filter)
    if total_ret.is_err:
        return Result.err(total_ret.err_value)

    ids_ret = repository.get_ids(filter, ExcludeOption(), SortOption(), PageOption(limit=limit, offset=offset))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    objs_ret = repository.bulk_get(ids=ids_ret.ok_value)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    data = [replace(o,
        image=create_url(o.image),
        video=create_url(o.video),
    ) for o in objs_ret.ok_value]

    return Result.ok((data, total_ret.ok_value))


@Result.shield_exception()
def get_manage_advertise(user_id: int, ulid: str) -> Result[AdvertiseData, NotFoundError | FatalError]:
    repository = injector.get(AdvertiseInterface)
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
    ))


@Result.shield_exception()
def create_manage_advertise(user_id: int, input: AdvertiseIn, image: UploadedFile, video: UploadedFile | None) -> Result[AdvertiseData, NotFoundError | FatalError]:
    repository = injector.get(AdvertiseInterface)

    count_ret = repository.count(FilterOption(owner_id=user_id))
    if count_ret.is_err:
        return Result.err(count_ret.err_value)

    count = count_ret.ok_value
    if count >= ADVERTISE_PERSONAL_LIMIT:
        log.error("Advertise limit exceeded", user_id=user_id, count=count)
        return Result.err(NotFoundError("作成に失敗しました!"))

    user = get_user_data(user_id=user_id)
    if user is None:
        log.error("User not found", user_id=user_id)
        return Result.err(NotFoundError("作成に失敗しました!"))

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
        new_ids_ret = repository.bulk_save([new_advertise])
        if new_ids_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(new_ids_ret.err_value)

        new_ids = new_ids_ret.ok_value
        assert len(new_ids) == 1, "作成に失敗しました"

    objs_ret = repository.bulk_get(new_ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    return Result.ok(objs_ret.ok_value[0])


@Result.shield_exception()
def update_manage_advertise(user_id: int, ulid: str, input: AdvertiseUpdateIn, image: UploadedFile | None, video: UploadedFile | None) -> Result[None, NotFoundError | FatalError]:
    repository = injector.get(AdvertiseInterface)
    ids_ret = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.error("Advertise not found", ulid=ulid, user_id=user_id)
        return Result.err(NotFoundError("保存に失敗しました!"))

    objs_ret = repository.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    obj = objs_ret.ok_value[0]

    user = get_user_data(user_id=user_id)
    if user is None:
        log.error("User not found", user_id=user_id)
        return Result.err(NotFoundError("保存に失敗しました!"))

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
        save_ret = repository.bulk_save([update_data])
        if save_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(save_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_manage_advertise(user_id: int, ulids: list[str]) -> Result[None, NotFoundError | FatalError]:
    repository = injector.get(AdvertiseInterface)
    ids: list[int] = []
    for ulid in ulids:
        target_ret = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption(), PageOption())
        if target_ret.is_err:
            return Result.err(target_ret.err_value)

        target = target_ret.ok_value
        if len(target) == 0:
            log.error("Advertise not found", ulid=ulid, user_id=user_id)
            return Result.err(NotFoundError("削除に失敗しました!"))
        ids.extend(target)

    delete_ret = repository.bulk_delete(ids)
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    return Result.ok(None)
