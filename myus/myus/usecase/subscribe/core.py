from myus.domain.channel.data import ChannelData
from myus.domain.channel.interface import ChannelInterface
from myus.domain.subscribe.interface import FilterOption, SortOption, SubscribeInterface
from myus.injectors.container import injector
from myus.utils.common.result import FatalError, FindError, NotFoundError, Result
from myus.utils.functions.transaction import atomic_result
from ._convert import save_subscribe_data
from ..channel.core import get_channel_data
from ..dto.subscribe import SubscribeDTO


@Result.shield_exception()
def get_subscribe_channels(user_id: int) -> Result[list[ChannelData], FatalError]:
    channel_repo = injector.get(ChannelInterface)
    repo = injector.get(SubscribeInterface)
    ids_ret = repo.get_ids(FilterOption(user_id=user_id, is_subscribe=True), SortOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    subscribe_ids = ids_ret.ok_value
    if len(subscribe_ids) == 0:
        return Result.ok([])

    subscribes_ret = repo.bulk_get(subscribe_ids)
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
    repo = injector.get(SubscribeInterface)
    channel_ret = get_channel_data(channel_ulid)
    if channel_ret.is_err:
        return Result.err(channel_ret.err_value)

    channel = channel_ret.ok_value
    if channel is None:
        return Result.err(NotFoundError("error.channelNotFound"))

    ids_ret = repo.get_ids(FilterOption(user_id=user_id, channel_id=channel.id), SortOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    subscribes_ret = repo.bulk_get(ids)
    if subscribes_ret.is_err:
        return Result.err(subscribes_ret.err_value)

    subscribes = subscribes_ret.ok_value
    subscribe = subscribes[0] if len(subscribes) > 0 else None

    save_ret = atomic_result(lambda: save_subscribe_data(user_id, channel.id, subscribe, is_subscribe))
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    count = save_ret.ok_value
    return Result.ok(SubscribeDTO(is_subscribe=is_subscribe, count=count))
