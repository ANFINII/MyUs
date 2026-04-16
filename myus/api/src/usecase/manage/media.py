from dataclasses import replace
from api.modules.logger import log
from api.src.domain.interface.media.video.data import VideoData
from api.src.domain.interface.media.video.interface import VideoInterface
from api.src.domain.interface.media.index import FilterOption, SortOption, ExcludeOption
from api.src.injectors.container import injector
from api.src.types.schema.media import VideoUpdateIn
from api.utils.functions.index import create_url


def get_manage_videos(user_id: int, search: str) -> list[VideoData]:
    repository = injector.get(VideoInterface)
    filter = FilterOption(search=search, owner_id=user_id)
    ids = repository.get_ids(filter, ExcludeOption(), SortOption())
    objs = repository.bulk_get(ids=ids)

    data = [replace(o,
        image=create_url(o.image),
        video=create_url(o.video),
        convert=create_url(o.convert),
    ) for o in objs]

    return data


def get_manage_video(user_id: int, ulid: str) -> VideoData | None:
    repository = injector.get(VideoInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption())
    if len(ids) == 0:
        log.info("Video not found", ulid=ulid, user_id=user_id)
        return None

    obj = repository.bulk_get(ids)[0]
    return replace(obj,
        image=create_url(obj.image),
        video=create_url(obj.video),
        convert=create_url(obj.convert),
    )


def update_manage_video(user_id: int, ulid: str, input: VideoUpdateIn) -> bool:
    repository = injector.get(VideoInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid), ExcludeOption(), SortOption())
    if len(ids) == 0:
        log.error("Video not found", ulid=ulid)
        return False

    obj = repository.bulk_get(ids)[0]
    if obj.channel.owner_id != user_id:
        log.error("Video owner mismatch", ulid=ulid, user_id=user_id, owner_id=obj.channel.owner_id)
        return False

    update_data = replace(obj, title=input.title, content=input.content, publish=input.publish)
    try:
        repository.bulk_save([update_data])
        return True
    except Exception as e:
        log.error("update_manage_video error", exc=e)
        return False


def delete_manage_video(user_id: int, ulid: str) -> bool:
    repository = injector.get(VideoInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid), ExcludeOption(), SortOption())
    if len(ids) == 0:
        log.error("Video not found", ulid=ulid)
        return False

    obj = repository.bulk_get(ids)[0]
    if obj.channel.owner_id != user_id:
        log.error("Video owner mismatch", ulid=ulid, user_id=user_id, owner_id=obj.channel.owner_id)
        return False

    try:
        repository.delete(obj.id)
        return True
    except Exception as e:
        log.error("delete_manage_video error", exc=e)
        return False
