from dataclasses import replace
from api.modules.logger import log
from api.src.domain.interface.media.video.data import VideoData
from api.src.domain.interface.media.video.interface import VideoInterface
from api.src.domain.interface.media.music.data import MusicData
from api.src.domain.interface.media.music.interface import MusicInterface
from api.src.domain.interface.media.index import FilterOption, SortOption, ExcludeOption
from api.src.injectors.container import injector
from api.src.types.schema.media.input import MusicUpdateIn, VideoUpdateIn
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


def delete_manage_video(user_id: int, ulids: list[str]) -> bool:
    repository = injector.get(VideoInterface)
    delete_ids: list[int] = []

    for ulid in ulids:
        ids = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption())
        if len(ids) == 0:
            log.error("Video not found or owner mismatch", ulid=ulid, user_id=user_id)
            return False
        delete_ids.append(ids[0])

    try:
        repository.bulk_delete(delete_ids)
        return True
    except Exception as e:
        log.error("delete_manage_video error", exc=e)
        return False


def get_manage_musics(user_id: int, search: str) -> list[MusicData]:
    repository = injector.get(MusicInterface)
    filter = FilterOption(search=search, owner_id=user_id)
    ids = repository.get_ids(filter, ExcludeOption(), SortOption())
    objs = repository.bulk_get(ids=ids)

    data = [replace(o, music=create_url(o.music)) for o in objs]
    return data


def get_manage_music(user_id: int, ulid: str) -> MusicData | None:
    repository = injector.get(MusicInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption())
    if len(ids) == 0:
        log.info("Music not found", ulid=ulid, user_id=user_id)
        return None

    obj = repository.bulk_get(ids)[0]
    return replace(obj, music=create_url(obj.music))


def update_manage_music(user_id: int, ulid: str, input: MusicUpdateIn) -> bool:
    repository = injector.get(MusicInterface)
    ids = repository.get_ids(FilterOption(ulid=ulid), ExcludeOption(), SortOption())
    if len(ids) == 0:
        log.error("Music not found", ulid=ulid)
        return False

    obj = repository.bulk_get(ids)[0]
    if obj.channel.owner_id != user_id:
        log.error("Music owner mismatch", ulid=ulid, user_id=user_id, owner_id=obj.channel.owner_id)
        return False

    update_data = replace(obj, title=input.title, content=input.content, lyric=input.lyric, download=input.download, publish=input.publish)
    try:
        repository.bulk_save([update_data])
        return True
    except Exception as e:
        log.error("update_manage_music error", exc=e)
        return False


def delete_manage_music(user_id: int, ulids: list[str]) -> bool:
    repository = injector.get(MusicInterface)
    delete_ids: list[int] = []

    for ulid in ulids:
        ids = repository.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption())
        if len(ids) == 0:
            log.error("Music not found or owner mismatch", ulid=ulid, user_id=user_id)
            return False
        delete_ids.append(ids[0])

    try:
        repository.bulk_delete(delete_ids)
        return True
    except Exception as e:
        log.error("delete_manage_music error", exc=e)
        return False
