from myus.domain.channel.data import ChannelData
from myus.domain.channel.interface import ChannelInterface
from myus.injectors.container import injector
from myus.utils.common.result import FatalError, Result


@Result.shield_exception()
def save_channel_data(data: ChannelData) -> Result[None, FatalError]:
    repo = injector.get(ChannelInterface)
    ret = repo.bulk_save([data])
    if ret.is_err:
        return Result.err(ret.err_value)

    return Result.ok(None)
