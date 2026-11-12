from dataclasses import replace
from datetime import timedelta
from django.utils import timezone
from myus.domain.access_log.data import AccessLogData
from myus.domain.access_log.interface import AccessLogInterface, FilterOption, SortOption
from myus.injectors.container import injector
from myus.utils.common.result import FatalError, Result
from myus.utils.enum.access_log import AccessType


ACCESS_INTERVAL = timedelta(hours=2)


@Result.shield_exception()
def save_access_data(ip_address: str, access_type: AccessType, type_id: int) -> Result[bool, FatalError]:
    repo = injector.get(AccessLogInterface)
    now = timezone.now()
    ids_ret = repo.get_ids(FilterOption(ip_address=ip_address, type=access_type, type_id=type_id), SortOption(), limit=1)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        create_ret = repo.bulk_save([AccessLogData(id=0, ip_address=ip_address, type=access_type, type_id=type_id, updated=now)])
        if create_ret.is_err:
            return Result.err(create_ret.err_value)

        return Result.ok(True)

    access_logs_ret = repo.bulk_get(ids)
    if access_logs_ret.is_err:
        return Result.err(access_logs_ret.err_value)

    access_logs = access_logs_ret.ok_value
    access_log = access_logs[0]
    if now - access_log.updated < ACCESS_INTERVAL:
        return Result.ok(False)

    save_ret = repo.bulk_save([replace(access_log, updated=now)])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(True)
