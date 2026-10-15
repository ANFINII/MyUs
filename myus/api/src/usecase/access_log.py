from dataclasses import replace
from datetime import timedelta
from django.utils import timezone
from api.src.domain.interface.access_log.data import AccessLogData
from api.src.domain.interface.access_log.interface import AccessLogInterface, FilterOption, SortOption
from api.src.injectors.container import injector
from api.utils.enum.media import MediaType


ACCESS_INTERVAL = timedelta(hours=2)


def record_access(ip_address: str, media_type: MediaType, media_id: int) -> bool:
    repository = injector.get(AccessLogInterface)
    now = timezone.now()
    ids = repository.get_ids(FilterOption(ip_address=ip_address, type=media_type, type_id=media_id), SortOption(), limit=1)
    if len(ids) == 0:
        repository.bulk_save([AccessLogData(id=0, ip_address=ip_address, type=media_type, type_id=media_id, updated=now)])
        return True

    access_log = repository.bulk_get(ids)[0]
    if now - access_log.updated < ACCESS_INTERVAL:
        return False

    repository.bulk_save([replace(access_log, updated=now)])
    return True
