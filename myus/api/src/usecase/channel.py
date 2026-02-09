from api.modules.logger import log
from api.src.domain.entity.channel.repository import ChannelRepository
from api.src.domain.interface.channel.data import ChannelData
from api.src.domain.interface.channel.interface import FilterOption, SortOption



def get_channel(ulid: str) -> ChannelData | None:
    repository = ChannelRepository()
    ids = repository.get_ids(FilterOption(ulid=ulid), SortOption())
    if len(ids) == 0:
        log.error("Channel not found", ulid=ulid)
        return None

    data = repository.bulk_get(ids)[0]
    return data


def get_user_channels(owner_id: int) -> list[ChannelData]:
    repository = ChannelRepository()
    ids = repository.get_ids(FilterOption(owner_id=owner_id), SortOption())
    if len(ids) == 0:
        log.warning("Channel not found", owner_id=owner_id)
        return []

    data = repository.bulk_get(ids)
    return data
