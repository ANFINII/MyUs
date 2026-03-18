from dataclasses import replace
from ninja import UploadedFile
from api.modules.logger import log
from api.src.domain.interface.channel.data import ChannelData
from api.src.domain.interface.channel.interface import ChannelInterface, FilterOption, SortOption
from api.src.injectors.container import injector
from api.src.types.schema.setting import SettingChannelIn
from api.utils.enum.index import ImageUpload
from api.utils.functions.media import save_upload



def get_channel(ulid: str) -> ChannelData | None:
    repository = injector.get(ChannelInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid), SortOption())
    if len(ids) == 0:
        log.error("Channel not found", ulid=ulid)
        return None

    data = repository.bulk_get(ids)[0]
    return data


def get_user_channels(owner_id: int) -> list[ChannelData]:
    repository = injector.get(ChannelInterface)
    ids = repository.get_ids(FilterOption(owner_id=owner_id), SortOption())
    if len(ids) == 0:
        log.warning("Channel not found", owner_id=owner_id)
        return []

    data = repository.bulk_get(ids)
    return data


def update_channel(user_id: int, ulid: str, input: SettingChannelIn, avatar_file: UploadedFile) -> bool:
    repository = injector.get(ChannelInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid), SortOption())
    if len(ids) == 0:
        log.error("Channel not found", ulid=ulid)
        return False

    channel = repository.bulk_get(ids)[0]
    if channel.owner_id != user_id:
        log.error("Channel owner mismatch", ulid=ulid, user_id=user_id, owner_id=channel.owner_id)
        return False

    avatar = save_upload(avatar_file, ImageUpload.CHANNEL, channel.ulid) if avatar_file else channel.avatar
    update_data = replace(channel, avatar=avatar, name=input.name, description=input.description)
    repository.bulk_save([update_data])
    return True
