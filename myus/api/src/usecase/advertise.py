import random
from dataclasses import replace
from datetime import date
from django.utils import timezone
from api.modules.logger import log
from api.src.domain.interface.advertise.data import AdvertiseData
from api.src.domain.interface.advertise.interface import AdvertiseInterface
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, PageOption, SortOption
from api.src.injectors.container import injector
from api.src.usecase.user import get_user_data
from api.utils.functions.index import create_url


def get_user_advertises(user_ulid: str) -> list[AdvertiseData]:
    user = get_user_data(ulid=user_ulid)
    if user is None:
        log.info("User not found", user_ulid=user_ulid)
        return []

    max_count = user.user_plan.plan.max_advertise
    if max_count <= 0:
        return []

    repository = injector.get(AdvertiseInterface)
    ids = repository.get_ids(FilterOption(owner_id=user.user.id, publish=True), ExcludeOption(), SortOption(), PageOption())
    if len(ids) == 0:
        return []

    objs = repository.bulk_get(ids)
    today = timezone.now().date()
    active = [o for o in objs if is_active(o, today)]
    if len(active) == 0:
        return []

    sample_size = min(max_count, len(active))
    picked = random.sample(active, sample_size)
    return [replace(a, image=create_url(a.image), video=create_url(a.video)) for a in picked]


def increment_advertise_read(ulid: str) -> int | None:
    repository = injector.get(AdvertiseInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid, publish=True), ExcludeOption(), SortOption(), PageOption())
    if len(ids) == 0:
        log.info("Advertise not found", ulid=ulid)
        return None

    obj = repository.bulk_get(ids)[0]
    updated = replace(obj, read=obj.read + 1)
    repository.bulk_save([updated])
    return updated.read


def is_active(ad: AdvertiseData, today: date) -> bool:
    if ad.type != "one":
        return False
    if ad.period is None:
        return True
    return ad.period >= today
