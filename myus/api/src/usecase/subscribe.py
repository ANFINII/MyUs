from dataclasses import replace
from django.db import transaction
from api.modules.logger import log
from api.src.domain.interface.channel.interface import ChannelInterface, FilterOption as ChannelFilterOption, SortOption as ChannelSortOption
from api.src.domain.interface.subscribe.data import SubscribeData
from api.src.domain.interface.subscribe.interface import FilterOption, SortOption, SubscribeInterface
from api.src.injectors.container import injector
from api.src.types.data.subscribe import SubscribeOutData


def upsert_subscribe(user_id: int, channel_ulid: str, is_subscribe: bool) -> SubscribeOutData | None:
    channel_repo = injector.get(ChannelInterface)
    subscribe_repo = injector.get(SubscribeInterface)
    channel_ids = channel_repo.get_ids(ChannelFilterOption(ulid=channel_ulid), ChannelSortOption())
    if len(channel_ids) == 0:
        log.info("チャンネルが見つかりません", ulid=channel_ulid)
        return None

    channel = channel_repo.bulk_get(channel_ids)[0]
    subscribe_ids = subscribe_repo.get_ids(FilterOption(user_id=user_id, channel_id=channel.id), SortOption())
    subscribes = subscribe_repo.bulk_get(subscribe_ids)
    subscribe = subscribes[0] if len(subscribes) > 0 else None

    with transaction.atomic():
        if subscribe is None:
            subscribe_repo.bulk_save([SubscribeData(
                id=0,
                user_id=user_id,
                channel_id=channel.id,
                is_subscribe=is_subscribe,
            )])
        else:
            updated_subscribe = replace(subscribe, is_subscribe=is_subscribe)
            subscribe_repo.bulk_save([updated_subscribe])

        count = subscribe_repo.count(FilterOption(channel_id=channel.id, is_subscribe=True))
        updated_channel = replace(channel, count=count)
        channel_repo.bulk_save([updated_channel])

    return SubscribeOutData(is_subscribe=is_subscribe, count=count)
