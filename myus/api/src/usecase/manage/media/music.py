from dataclasses import replace
from api.modules.logger import log
from api.src.domain.interface.media.music.data import MusicData
from api.src.domain.interface.media.music.interface import MusicInterface
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, PAGE_SIZE, PageOption, SortOption
from api.src.injectors.container import injector
from api.src.types.schema.media.input import MusicUpdateIn
from api.src.usecase.category import get_category_data
from api.src.usecase.notification import create_publish_notification
from api.src.usecase.manage.media._data import save_music_data, delete_music_data
from api.utils.common.result import FatalError, FindError, ForbiddenError, NotFoundError, Result, ValidationError, WriteError
from api.utils.enum.notification import NotificationObjectType, NotificationTypeNo
from api.utils.functions.index import create_url
from api.utils.functions.transaction import atomic_result


@Result.shield_exception()
def get_manage_musics(user_id: int, search: str, channel_ulid: str = "", limit: int = PAGE_SIZE, offset: int = 0) -> Result[tuple[list[MusicData], int], FatalError]:
    repo = injector.get(MusicInterface)
    filter = FilterOption(search=search, owner_id=user_id, channel_ulid=channel_ulid)
    count_ret = repo.count(filter)
    if count_ret.is_err:
        return Result.err(count_ret.err_value)

    total = count_ret.ok_value
    ids_ret = repo.get_ids(filter, ExcludeOption(), SortOption(), PageOption(limit=limit, offset=offset))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    objs_ret = repo.bulk_get(ids=ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value

    data = [replace(o, music=create_url(o.music)) for o in objs]
    return Result.ok((data, total))


@Result.shield_exception()
def get_manage_music(user_id: int, ulid: str) -> Result[MusicData, FindError]:
    repo = injector.get(MusicInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid, owner_id=user_id), ExcludeOption(), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.info("data not found", ulid=ulid, user_id=user_id)
        return Result.err(NotFoundError("data not found"))

    objs_ret = repo.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]
    return Result.ok(replace(obj, music=create_url(obj.music)))


@Result.shield_exception()
def update_manage_music(user_id: int, ulid: str, input: MusicUpdateIn) -> Result[None, WriteError]:
    repo = injector.get(MusicInterface)
    ids_ret = repo.get_ids(FilterOption(ulid=ulid), ExcludeOption(), SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.error("Music not found", ulid=ulid)
        return Result.err(NotFoundError("error.saveFailed"))

    objs_ret = repo.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    obj = objs[0]
    if obj.channel.owner_id != user_id:
        log.error("Music owner mismatch", ulid=ulid, user_id=user_id, owner_id=obj.channel.owner_id)
        return Result.err(ForbiddenError("error.saveFailed"))

    update_data = replace(obj, title=input.title, content=input.content, lyric=input.lyric, download=input.download, publish=input.publish, publish_at=input.publish_at)
    category_data_ret = get_category_data(input.category_ulid)
    if category_data_ret.is_err:
        return Result.err(category_data_ret.err_value)

    category_data = category_data_ret.ok_value
    if category_data is None:
        return Result.err(ValidationError("error.categoryRequired"))

    save_ret = atomic_result(lambda: save_music_data(update_data, category_data))
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    if not obj.publish and input.publish:
        notification_ret = create_publish_notification(user_id, NotificationTypeNo.MUSIC, obj.id, NotificationObjectType.MUSIC)
        if notification_ret.is_err:
            return Result.err(notification_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_manage_music(user_id: int, ulids: list[str]) -> Result[None, FindError]:
    repo = injector.get(MusicInterface)
    ids_ret = repo.get_ids(FilterOption(ulids=ulids, owner_id=user_id), ExcludeOption(), SortOption(), PageOption(limit=len(ulids)))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    delete_ids = ids_ret.ok_value
    if len(delete_ids) != len(set(ulids)):
        log.error("Music not found or owner mismatch", ulids=ulids, user_id=user_id)
        return Result.err(NotFoundError("error.deleteFailed"))

    delete_ret = atomic_result(lambda: delete_music_data(delete_ids))
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    return Result.ok(None)
