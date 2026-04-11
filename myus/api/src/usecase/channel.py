from dataclasses import replace
from django_ulid.models import ulid
from ninja import UploadedFile
from api.modules.logger import log
from api.src.domain.interface.channel.data import ChannelData
from api.src.domain.interface.channel.interface import ChannelInterface, FilterOption, SortOption
from api.src.injectors.container import injector
from api.src.types.schema.channel import ChannelIn
from api.utils.enum.index import ImageUpload
from api.utils.functions.media import save_upload


def get_channel_data(ulid: str) -> ChannelData | None:
    repository = injector.get(ChannelInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid), SortOption())
    if len(ids) == 0:
        log.error("Channel not found", ulid=ulid)
        return None

    data = repository.bulk_get(ids)[0]
    return data


def save_channel_data(data: ChannelData) -> bool:
    repository = injector.get(ChannelInterface)
    try:
        repository.bulk_save([data])
        return True
    except Exception as e:
        log.error("save_channel_data error", exc=e)
        return False


def get_user_channels(owner_id: int) -> list[ChannelData]:
    repository = injector.get(ChannelInterface)
    ids = repository.get_ids(FilterOption(owner_id=owner_id), SortOption())
    if len(ids) == 0:
        log.warning("Channel not found", owner_id=owner_id)
        return []

    return repository.bulk_get(ids)


def create_user_channel(user_id: int, input: ChannelIn, avatar_file: UploadedFile) -> str | None:
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

    try:
        repository.bulk_save([data])
        return new_ulid
    except Exception as e:
        log.error("create_user_channel error", exc=e)
        return None


def update_user_channel(user_id: int, ulid: str, input: ChannelIn, avatar_file: UploadedFile) -> bool:
    channel = get_channel_data(ulid)
    if channel is None:
        return False

    if channel.owner_id != user_id:
        log.error("Channel owner mismatch", ulid=ulid, user_id=user_id, owner_id=channel.owner_id)
        return False

    avatar = save_upload(avatar_file, ImageUpload.CHANNEL, channel.ulid) if avatar_file else channel.avatar
    update_data = replace(channel, avatar=avatar, name=input.name, description=input.description)
    return save_channel_data(update_data)
