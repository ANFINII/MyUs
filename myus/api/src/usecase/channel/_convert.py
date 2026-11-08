from api.src.domain.interface.channel.data import ChannelData
from api.src.domain.interface.channel.interface import ChannelInterface
from api.src.injectors.container import injector
from api.utils.common.result import FatalError, Result


@Result.shield_exception()
def save_channel_data(data: ChannelData) -> Result[None, FatalError]:
    repo = injector.get(ChannelInterface)
    ret = repo.bulk_save([data])
    if ret.is_err:
        return Result.err(ret.err_value)

    return Result.ok(None)
