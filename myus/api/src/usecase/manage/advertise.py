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
from api.utils.enum.index import ImageUpload, MediaUpload
from api.utils.functions.index import create_url
from api.utils.functions.media import save_upload


ADVERTISE_TYPE_PERSONAL = "one"
ADVERTISE_PERSONAL_LIMIT = 5


def get_manage_advertises(user_id: int, search: str, limit: int = PAGE_SIZE, offset: int = 0) -> tuple[list[AdvertiseData], int]:
    repository = injector.get(AdvertiseInterface)
    filter = FilterOption(search=search, owner_id=user_id)
    total = repository.count(filter)
    ids = repository.get_ids(filter, ExcludeOption(), SortOption(), PageOption(limit=limit, offset=offset))
    objs = repository.bulk_get(ids=ids)

    data = [replace(o,
        image=create_url(o.image),
        video=create_url(o.video),
    ) for o in objs]

    return data, total


def get_manage_advertise(user_id: int, ulid: str) -> AdvertiseData | None:
    repository = injector.get(AdvertiseInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption(), PageOption())
    if len(ids) == 0:
        log.info("Advertise not found", ulid=ulid, user_id=user_id)
        return None

    obj = repository.bulk_get(ids)[0]
    return replace(obj,
        image=create_url(obj.image),
        video=create_url(obj.video),
    )


def create_manage_advertise(user_id: int, input: AdvertiseIn, image: UploadedFile, video: UploadedFile | None) -> AdvertiseData | None:
    repository = injector.get(AdvertiseInterface)

    count = repository.count(FilterOption(owner_id=user_id))
    if count >= ADVERTISE_PERSONAL_LIMIT:
        log.error("Advertise limit exceeded", user_id=user_id, count=count)
        return None

    user = get_user_data(user_id=user_id)
    if user is None:
        log.error("User not found", user_id=user_id)
        return None

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
        new_ids = repository.bulk_save([new_advertise])
        assert len(new_ids) == 1, "作成に失敗しました"

    return repository.bulk_get(new_ids)[0]


def update_manage_advertise(user_id: int, ulid: str, input: AdvertiseUpdateIn, image: UploadedFile | None, video: UploadedFile | None) -> bool:
    repository = injector.get(AdvertiseInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption(), PageOption())
    if len(ids) == 0:
        log.error("Advertise not found", ulid=ulid, user_id=user_id)
        return False

    obj = repository.bulk_get(ids)[0]

    user = get_user_data(user_id=user_id)
    if user is None:
        log.error("User not found", user_id=user_id)
        return False

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

    try:
        with transaction.atomic():
            repository.bulk_save([update_data])
    except Exception as e:
        log.error("Advertise update failed", ulid=ulid, error=str(e))
        return False

    return True


def delete_manage_advertise(user_id: int, ulids: list[str]) -> bool:
    repository = injector.get(AdvertiseInterface)
    ids: list[int] = []
    for ulid in ulids:
        target = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption(), PageOption())
        if len(target) == 0:
            log.error("Advertise not found", ulid=ulid, user_id=user_id)
            return False
        ids.extend(target)

    repository.bulk_delete(ids)
    return True
