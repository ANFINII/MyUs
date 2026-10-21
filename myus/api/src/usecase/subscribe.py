from dataclasses import replace
from django.db import transaction
from api.src.domain.interface.channel.data import ChannelData
from api.src.domain.interface.channel.interface import ChannelInterface
from api.src.domain.interface.subscribe.data import SubscribeData
from api.src.domain.interface.subscribe.interface import FilterOption, SortOption, SubscribeInterface
from api.src.injectors.container import injector
from api.src.types.dto.subscribe import SubscribeDTO
from api.src.usecase.channel import get_channel_data
from api.utils.common.result import FatalError, FindError, NotFoundError, Result


@Result.shield_exception()
def get_subscribe_channels(user_id: int) -> Result[list[ChannelData], FatalError]:
    channel_repo = injector.get(ChannelInterface)
    subscribe_repo = injector.get(SubscribeInterface)
    ids_ret = subscribe_repo.get_ids(FilterOption(user_id=user_id, is_subscribe=True), SortOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    subscribe_ids = ids_ret.ok_value
    if len(subscribe_ids) == 0:
        return Result.ok([])

    subscribes_ret = subscribe_repo.bulk_get(subscribe_ids)
    if subscribes_ret.is_err:
        return Result.err(subscribes_ret.err_value)

    subscribes = subscribes_ret.ok_value
    channel_ids = [s.channel_id for s in subscribes]
    channels_ret = channel_repo.bulk_get(channel_ids)
    if channels_ret.is_err:
        return Result.err(channels_ret.err_value)

    channels = channels_ret.ok_value
    return Result.ok(channels)


@Result.shield_exception()
def upsert_subscribe(user_id: int, channel_ulid: str, is_subscribe: bool) -> Result[SubscribeDTO, FindError]:
    channel_repo = injector.get(ChannelInterface)
    subscribe_repo = injector.get(SubscribeInterface)
    channel_ret = get_channel_data(channel_ulid)
    if channel_ret.is_err:
        return Result.err(channel_ret.err_value)

    channel = channel_ret.ok_value
    if channel is None:
        return Result.err(NotFoundError("チャンネルが見つかりません!"))

    ids_ret = subscribe_repo.get_ids(FilterOption(user_id=user_id, channel_id=channel.id), SortOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    subscribes_ret = subscribe_repo.bulk_get(ids)
    if subscribes_ret.is_err:
        return Result.err(subscribes_ret.err_value)

    subscribes = subscribes_ret.ok_value
    subscribe = subscribes[0] if len(subscribes) > 0 else None

    with transaction.atomic():
        if subscribe is None:
            save_ret = subscribe_repo.bulk_save([SubscribeData(
                id=0,
                user_id=user_id,
                channel_id=channel.id,
                is_subscribe=is_subscribe,
            )])
        else:
            updated_subscribe = replace(subscribe, is_subscribe=is_subscribe)
            save_ret = subscribe_repo.bulk_save([updated_subscribe])

        if save_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(save_ret.err_value)

        count_ret = subscribe_repo.count(FilterOption(channel_id=channel.id, is_subscribe=True))
        if count_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(count_ret.err_value)

        count = count_ret.ok_value
        channel_count_ret = channel_repo.update_count(channel.id, count)
        if channel_count_ret.is_err:
            transaction.set_rollback(True)
            return Result.err(channel_count_ret.err_value)

    return Result.ok(SubscribeDTO(is_subscribe=is_subscribe, count=count))
