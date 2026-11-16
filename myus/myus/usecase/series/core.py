from dataclasses import replace
from myus.domain.media.common import FilterOption as MediaFilterOption, PageOption as MediaPageOption, SortOption as MediaSortOption
from myus.domain.series.data import SeriesData
from myus.domain.series.interface import FilterOption, SeriesInterface
from myus.injectors.container import injector
from myus.utils.common.logger import log
from myus.utils.common.result import AccessError, FindError, ForbiddenError, NotFoundError, Result
from myus.utils.functions.common import create_url
from ._convert import get_own_series_data, get_published_media_data, get_series_items_data, get_series_list_data, media_image
from ..channel.core import get_channel_data
from ..dto.series import ChannelSeriesDTO, SeriesCreateDTO, SeriesDetailDTO, SeriesDTO, SeriesUpdateDTO
from ..media._convert import get_media_repository


@Result.shield_exception()
def get_channel_series(channel_ulid: str) -> Result[list[ChannelSeriesDTO], FindError]:
    channel_ret = get_channel_data(channel_ulid)
    if channel_ret.is_err:
        return Result.err(channel_ret.err_value)

    channel = channel_ret.ok_value
    if channel is None:
        log.info("not found", channel_ulid=channel_ulid)
        return Result.err(NotFoundError("error.channelNotFound"))

    series_ret = get_series_list_data(FilterOption(channel_id=channel.id))
    if series_ret.is_err:
        return Result.err(series_ret.err_value)

    series_list = series_ret.ok_value
    data: list[ChannelSeriesDTO] = []
    for series in series_list:
        medias_ret = get_published_media_data(series.media_type, series.media_ids)
        if medias_ret.is_err:
            return Result.err(medias_ret.err_value)

        medias = medias_ret.ok_value
        if len(medias) == 0:
            continue

        first = medias[0]
        image = media_image(first) or channel.avatar
        data.append(ChannelSeriesDTO(ulid=series.ulid, title=series.title, media_type=series.media_type, count=len(medias), media_ulid=first.ulid, image=create_url(image)))

    return Result.ok(data)


@Result.shield_exception()
def get_manage_series_list(user_id: int, channel_ulid: str) -> Result[list[SeriesDTO], FindError]:
    channel_ret = get_channel_data(channel_ulid)
    if channel_ret.is_err:
        return Result.err(channel_ret.err_value)

    channel = channel_ret.ok_value
    if channel is None or channel.owner_id != user_id:
        log.info("not found", channel_ulid=channel_ulid, user_id=user_id)
        return Result.err(NotFoundError("error.channelNotFound"))

    series_ret = get_series_list_data(FilterOption(channel_id=channel.id))
    if series_ret.is_err:
        return Result.err(series_ret.err_value)

    series_list = series_ret.ok_value
    return Result.ok([SeriesDTO(ulid=s.ulid, title=s.title, media_type=s.media_type, count=len(s.media_ids)) for s in series_list])


@Result.shield_exception()
def create_manage_series(user_id: int, input: SeriesCreateDTO) -> Result[str, AccessError]:
    channel_ret = get_channel_data(input.channel_ulid)
    if channel_ret.is_err:
        return Result.err(channel_ret.err_value)

    channel = channel_ret.ok_value
    if channel is None:
        return Result.err(NotFoundError("error.channelNotFound"))

    if channel.owner_id != user_id:
        log.warning("owner mismatch", channel_ulid=channel.ulid, user_id=user_id)
        return Result.err(ForbiddenError("error.createFailed"))

    repo = injector.get(SeriesInterface)
    new_data = SeriesData(id=0, ulid="", channel_id=channel.id, media_type=input.media_type, title=input.title, media_ids=[])
    save_ret = repo.bulk_save([new_data])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    new_ids = save_ret.ok_value
    objs_ret = repo.bulk_get(new_ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    assert len(objs) == 1, "作成に失敗しました"
    return Result.ok(objs[0].ulid)


@Result.shield_exception()
def get_manage_series(user_id: int, ulid: str) -> Result[SeriesDetailDTO, AccessError]:
    own_ret = get_own_series_data(user_id, ulid, "error.mediaNotFound")
    if own_ret.is_err:
        return Result.err(own_ret.err_value)

    series, channel = own_ret.ok_value
    items_ret = get_series_items_data(series.media_type, series.media_ids)
    if items_ret.is_err:
        return Result.err(items_ret.err_value)

    items = items_ret.ok_value
    linked_ret = get_series_list_data(FilterOption(channel_id=channel.id, media_type=series.media_type))
    if linked_ret.is_err:
        return Result.err(linked_ret.err_value)

    linked_list = linked_ret.ok_value
    linked_ids = {media_id for s in linked_list for media_id in s.media_ids}
    media_repo = get_media_repository(series.media_type)
    channel_ids_ret = media_repo.get_ids(MediaFilterOption(channel_id=channel.id), MediaSortOption(), MediaPageOption(limit=0))
    if channel_ids_ret.is_err:
        return Result.err(channel_ids_ret.err_value)

    channel_ids = channel_ids_ret.ok_value
    candidates_ret = get_series_items_data(series.media_type, [i for i in channel_ids if i not in linked_ids])
    if candidates_ret.is_err:
        return Result.err(candidates_ret.err_value)

    candidates = candidates_ret.ok_value
    return Result.ok(SeriesDetailDTO(ulid=series.ulid, title=series.title, media_type=series.media_type, channel_ulid=channel.ulid, items=items, candidates=candidates))


@Result.shield_exception()
def update_manage_series(user_id: int, ulid: str, input: SeriesUpdateDTO) -> Result[None, AccessError]:
    own_ret = get_own_series_data(user_id, ulid, "error.saveFailed")
    if own_ret.is_err:
        return Result.err(own_ret.err_value)

    series, channel = own_ret.ok_value
    media_repo = get_media_repository(series.media_type)
    media_ids_ret = media_repo.get_ids(MediaFilterOption(ulids=input.media_ulids, channel_id=channel.id), MediaSortOption(), MediaPageOption(limit=0))
    if media_ids_ret.is_err:
        return Result.err(media_ids_ret.err_value)

    media_ids = media_ids_ret.ok_value
    medias_ret = media_repo.bulk_get(media_ids)
    if medias_ret.is_err:
        return Result.err(medias_ret.err_value)

    medias = medias_ret.ok_value
    ulid_map = {m.ulid: m.id for m in medias}
    if len(ulid_map) != len(set(input.media_ulids)):
        log.warning("channel mismatch", ulid=ulid, user_id=user_id)
        return Result.err(ForbiddenError("error.saveFailed"))

    others_ret = get_series_list_data(FilterOption(media_type=series.media_type, media_ids=list(ulid_map.values())))
    if others_ret.is_err:
        return Result.err(others_ret.err_value)

    others = others_ret.ok_value
    if any(o.id != series.id for o in others):
        log.warning("other series", ulid=ulid, user_id=user_id)
        return Result.err(ForbiddenError("error.saveFailed"))

    repo = injector.get(SeriesInterface)
    save_ret = repo.bulk_save([replace(series, title=input.title, media_ids=list(dict.fromkeys(ulid_map[u] for u in input.media_ulids)))])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def delete_manage_series(user_id: int, ulid: str) -> Result[None, AccessError]:
    own_ret = get_own_series_data(user_id, ulid, "error.deleteFailed")
    if own_ret.is_err:
        return Result.err(own_ret.err_value)

    series, _ = own_ret.ok_value
    repo = injector.get(SeriesInterface)
    delete_ret = repo.bulk_delete([series.id])
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    return Result.ok(None)
