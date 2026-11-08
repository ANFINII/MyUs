from datetime import date
from api.src.domain.interface.advertise.data import AdvertiseData
from api.src.domain.interface.advertise.interface import AdvertiseInterface
from api.src.injectors.container import injector
from api.src.usecase.access_log._convert import save_access_data
from api.utils.common.result import FatalError, Result
from api.utils.enum.access_log import AccessType


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
