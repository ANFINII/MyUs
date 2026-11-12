from dataclasses import replace
from myus.domain.interface.channel.interface import ChannelInterface
from myus.domain.interface.subscribe.data import SubscribeData
from myus.domain.interface.subscribe.interface import FilterOption, SubscribeInterface
from myus.injectors.container import injector
from myus.utils.common.result import FatalError, Result


@Result.shield_exception()
def save_subscribe_data(user_id: int, channel_id: int, subscribe: SubscribeData | None, is_subscribe: bool) -> Result[int, FatalError]:
    channel_repo = injector.get(ChannelInterface)
    repo = injector.get(SubscribeInterface)
    if subscribe is None:
        save_ret = repo.bulk_save([SubscribeData(
            id=0,
            user_id=user_id,
            channel_id=channel_id,
            is_subscribe=is_subscribe,
        )])
    else:
        updated_subscribe = replace(subscribe, is_subscribe=is_subscribe)
        save_ret = repo.bulk_save([updated_subscribe])

    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    count_ret = repo.count(FilterOption(channel_id=channel_id, is_subscribe=True))
    if count_ret.is_err:
        return Result.err(count_ret.err_value)

    count = count_ret.ok_value
    channel_count_ret = channel_repo.save_count(channel_id, count)
    if channel_count_ret.is_err:
        return Result.err(channel_count_ret.err_value)

    return Result.ok(count)
