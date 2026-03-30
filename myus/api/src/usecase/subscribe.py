from dataclasses import replace
from django.db import transaction
from api.src.domain.interface.channel.interface import ChannelInterface
from api.src.domain.interface.subscribe.data import SubscribeData
from api.src.domain.interface.subscribe.interface import FilterOption, SortOption, SubscribeInterface
from api.src.injectors.container import injector
from api.src.types.dto.subscribe import SubscribeDTO
from api.src.usecase.channel import get_channel_data


def upsert_subscribe(user_id: int, channel_ulid: str, is_subscribe: bool) -> SubscribeDTO | None:
    channel_repo = injector.get(ChannelInterface)
    subscribe_repo = injector.get(SubscribeInterface)
    channel = get_channel_data(channel_ulid)
    if channel is None:
        return None

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

    return SubscribeDTO(is_subscribe=is_subscribe, count=count)
