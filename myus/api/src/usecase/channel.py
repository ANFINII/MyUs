from api.db.models.channel import Channel
from api.modules.logger import log
from api.src.domain.channel import ChannelDomain, FilterOption, SortOption


def get_channel(ulid: str) -> Channel | None:
    ids = ChannelDomain.get_ids(FilterOption(ulid=ulid), SortOption())
    if len(ids) == 0:
        log.error("Channel not found", ulid=ulid)
        return None

    objs = ChannelDomain.bulk_get(ids)
    return objs[0]
