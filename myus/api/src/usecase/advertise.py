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
from api.utils.common.result import FatalError, FindError, NotFoundError, Result
from api.utils.functions.index import create_url
from api.utils.plan import get_plan


@Result.shield_exception()
def get_user_advertises(user_ulid: str) -> Result[list[AdvertiseData], FatalError]:
    user_ret = get_user_data(ulid=user_ulid)
    if user_ret.is_err:
        return Result.err(user_ret.err_value)

    user = user_ret.ok_value
    if user is None:
        log.info("User not found", user_ulid=user_ulid)
        return Result.ok([])

    plan = get_plan(user.user_plan.plan)
    max_count = plan.max_advertise if plan is not None else 0
    if max_count <= 0:
        return Result.ok([])

    repository = injector.get(AdvertiseInterface)
    ids_ret = repository.get_ids(FilterOption(owner_id=user.user.id, publish=True), ExcludeOption(), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        return Result.ok([])

    objs_ret = repository.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    today = timezone.localdate()
    active = [o for o in objs if is_active(o, today)]
    if len(active) == 0:
        return Result.ok([])

    sample_size = min(max_count, len(active))
    picked = random.sample(active, sample_size)
    return Result.ok([replace(a, image=create_url(a.image), video=create_url(a.video)) for a in picked])


@Result.shield_exception()
def increment_advertise_read(ulid: str) -> Result[int, FindError]:
    repository = injector.get(AdvertiseInterface)
    ids_ret = repository.get_ids(FilterOption(ulid=ulid, publish=True), ExcludeOption(), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.info("data not found", ulid=ulid)
        return Result.err(NotFoundError("data not found"))

    read_ret = repository.save_read(ids[0])
    if read_ret.is_err:
        return Result.err(read_ret.err_value)

    read = read_ret.ok_value
    return Result.ok(read)


def is_active(ad: AdvertiseData, today: date) -> bool:
    if ad.type != "one":
        return False
    if ad.period is None:
        return True
    return ad.period >= today
