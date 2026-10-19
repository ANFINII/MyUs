from dataclasses import replace
from django_ulid.models import ulid
from ninja import UploadedFile
from api.modules.logger import log
from api.src.domain.interface.channel.data import ChannelData
from api.src.domain.interface.channel.interface import ChannelInterface, FilterOption, SortOption, SortType
from api.src.injectors.container import injector
from api.src.types.schema.channel import ChannelIn
from api.utils.common.result import FatalError, ForbiddenError, NotFoundError, Result
from api.utils.enum.upload import ImageUpload
from api.utils.functions.media import save_upload


@Result.shield_exception()
def get_channel_data(ulid: str) -> Result[ChannelData | None, FatalError]:
    repository = injector.get(ChannelInterface)
    ids_ret = repository.get_ids(FilterOption(ulid=ulid), SortOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.error("Channel not found", ulid=ulid)
        return Result.ok(None)

    channels_ret = repository.bulk_get(ids)
    if channels_ret.is_err:
        return Result.err(channels_ret.err_value)

    channels = channels_ret.ok_value
    data = channels[0]
    return Result.ok(data)


@Result.shield_exception()
def save_channel_data(data: ChannelData) -> Result[None, FatalError]:
    repository = injector.get(ChannelInterface)
    ret = repository.bulk_save([data])
    if ret.is_err:
        return Result.err(ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def get_user_channels(owner_id: int) -> Result[list[ChannelData], FatalError]:
    repository = injector.get(ChannelInterface)
    ids_ret = repository.get_ids(FilterOption(owner_id=owner_id), SortOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.warning("Channel not found", owner_id=owner_id)
        return Result.ok([])

    channels_ret = repository.bulk_get(ids)
    if channels_ret.is_err:
        return Result.err(channels_ret.err_value)

    channels = channels_ret.ok_value
    return Result.ok(channels)


@Result.shield_exception()
def create_user_channel(user_id: int, input: ChannelIn, avatar_file: UploadedFile) -> Result[str, FatalError]:
    repository = injector.get(ChannelInterface)
    new_ulid = str(ulid.new())
    avatar = save_upload(avatar_file, ImageUpload.CHANNEL, new_ulid) if avatar_file else ""

    data = ChannelData(
        id=0,
        ulid=new_ulid,
        owner_id=user_id,
        owner_ulid="",
        avatar=avatar,
        name=input.name,
        description=input.description,
        is_default=False,
        count=0,
    )

    ret = repository.bulk_save([data])
    if ret.is_err:
        return Result.err(ret.err_value)

    return Result.ok(new_ulid)


@Result.shield_exception()
def update_user_channel(user_id: int, ulid: str, input: ChannelIn, avatar_file: UploadedFile) -> Result[None, NotFoundError | ForbiddenError | FatalError]:
    channel_ret = get_channel_data(ulid)
    if channel_ret.is_err:
        return Result.err(channel_ret.err_value)

    channel = channel_ret.ok_value
    if channel is None:
        return Result.err(NotFoundError("保存に失敗しました!"))

    if channel.owner_id != user_id:
        log.error("Channel owner mismatch", ulid=ulid, user_id=user_id, owner_id=channel.owner_id)
        return Result.err(ForbiddenError("保存に失敗しました!"))

    avatar = save_upload(avatar_file, ImageUpload.CHANNEL, channel.ulid) if avatar_file else channel.avatar
    update_data = replace(channel, avatar=avatar, name=input.name, description=input.description)
    save_ret = save_channel_data(update_data)
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(None)
