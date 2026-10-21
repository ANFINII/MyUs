from dataclasses import replace
from datetime import timedelta
from django.utils import timezone
from api.src.domain.interface.access_log.data import AccessLogData
from api.src.domain.interface.access_log.interface import AccessLogInterface, FilterOption, SortOption
from api.src.injectors.container import injector
from api.utils.common.result import FatalError, Result
from api.utils.enum.media import MediaType


ACCESS_INTERVAL = timedelta(hours=2)


@Result.shield_exception()
def record_access(ip_address: str, media_type: MediaType, media_id: int) -> Result[bool, FatalError]:
    repo = injector.get(AccessLogInterface)
    now = timezone.now()
    ids_ret = repo.get_ids(FilterOption(ip_address=ip_address, type=media_type, type_id=media_id), SortOption(), limit=1)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        create_ret = repo.bulk_save([AccessLogData(id=0, ip_address=ip_address, type=media_type, type_id=media_id, updated=now)])
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
