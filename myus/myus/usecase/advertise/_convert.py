from datetime import date
from myus.domain.advertise.data import AdvertiseData
from myus.domain.advertise.interface import AdvertiseInterface
from myus.injectors.container import injector
from myus.usecase.access_log._convert import save_access_data
from myus.utils.common.result import FatalError, Result
from myus.utils.enum.access_log import AccessType


@Result.shield_exception()
def save_read_data(advertise_id: int, read: int, ip_address: str) -> Result[int, FatalError]:
    repo = injector.get(AdvertiseInterface)
    access_ret = save_access_data(ip_address, AccessType.ADVERTISE, advertise_id)
    if access_ret.is_err:
        return Result.err(access_ret.err_value)

    is_accessed = access_ret.ok_value
    if not is_accessed:
        return Result.ok(read)

    read_ret = repo.save_read(advertise_id)
    if read_ret.is_err:
        return Result.err(read_ret.err_value)

    new_read = read_ret.ok_value
    return Result.ok(new_read)


def is_active(ad: AdvertiseData, today: date) -> bool:
    if ad.type != "one":
        return False
    if ad.period is None:
        return True
    return ad.period >= today
