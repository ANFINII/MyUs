from api.db.models.channel import Channel
from api.modules.logger import log
from api.src.domain.channel import ChannelDomain, FilterOption, SortOption


def get_channel(ulid: str) -> Channel | None:
    ids = ChannelDomain.get_ids(FilterOption(ulid=ulid), SortOption())
    if len(ids) == 0:
        log.error("Channel not found", ulid=ulid)
        return None

    data = ChannelDomain.bulk_get(ids)[0]
    return data


def get_user_channels(owner_id: int) -> list[Channel]:
    ids = ChannelDomain.get_ids(FilterOption(owner_id=owner_id), SortOption())
    if len(ids) == 0:
        log.warning("Channel not found", owner_id=owner_id)
        return []

    data = ChannelDomain.bulk_get(ids)
    return data
