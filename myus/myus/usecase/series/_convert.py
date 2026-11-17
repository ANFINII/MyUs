from dataclasses import replace
from myus.domain.channel.data import ChannelData
from myus.domain.channel.interface import ChannelInterface
from myus.domain.payment.plan import get_plan
from myus.domain.media.blog.data import BlogData
from myus.domain.media.chat.data import ChatData
from myus.domain.media.comic.data import ComicData
from myus.domain.media.common import FilterOption as MediaFilterOption, PageOption as MediaPageOption, SortOption as MediaSortOption
from myus.domain.media.music.data import MusicData
from myus.domain.media.picture.data import PictureData
from myus.domain.media.video.data import VideoData
from myus.domain.series.data import SeriesData
from myus.domain.series.interface import FilterOption, PageOption, SeriesInterface, SortOption
from myus.injectors.container import injector
from myus.utils.common.logger import log
from myus.utils.common.result import AccessError, FatalError, ForbiddenError, NotFoundError, Result
from myus.utils.enum.media import MediaType
from ..dto.series import MediaSeriesDTO, SeriesItemDTO
from ..media._convert import get_media_repository
from ..user.core import get_user_data


type MediaDataType = VideoData | MusicData | BlogData | ComicData | PictureData | ChatData


@Result.shield_exception()
def get_series_list_data(filter: FilterOption) -> Result[list[SeriesData], FatalError]:
    repo = injector.get(SeriesInterface)
    ids_ret = repo.get_ids(filter, SortOption(), PageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    objs_ret = repo.bulk_get(ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    return Result.ok(objs)


@Result.shield_exception()
def check_series_plan_data(user_id: int) -> Result[None, AccessError]:
    user_ret = get_user_data(user_id=user_id)
    if user_ret.is_err:
        return Result.err(user_ret.err_value)

    user = user_ret.ok_value
    plan = get_plan(user.user_plan.plan) if user is not None else None
    if plan is None or not plan.is_series:
        log.info("plan required", user_id=user_id)
        return Result.err(ForbiddenError("error.seriesPlanRequired"))

    return Result.ok(None)


@Result.shield_exception()
def get_own_series_data(user_id: int, ulid: str, error: str) -> Result[tuple[SeriesData, ChannelData], AccessError]:
    series_ret = get_series_list_data(FilterOption(ulid=ulid))
    if series_ret.is_err:
        return Result.err(series_ret.err_value)

    series_list = series_ret.ok_value
    if len(series_list) == 0:
        log.warning("not found", ulid=ulid)
        return Result.err(NotFoundError(error))

    series = series_list[0]
    channel_repo = injector.get(ChannelInterface)
    channels_ret = channel_repo.bulk_get([series.channel_id])
    if channels_ret.is_err:
        return Result.err(channels_ret.err_value)

    channels = channels_ret.ok_value
    if len(channels) == 0 or channels[0].owner_id != user_id:
        log.warning("owner mismatch", ulid=ulid, user_id=user_id)
        return Result.err(ForbiddenError(error))

    return Result.ok((series, channels[0]))


@Result.shield_exception()
def get_series_items_data(media_type: MediaType, media_ids: list[int]) -> Result[list[SeriesItemDTO], FatalError]:
    repo = get_media_repository(media_type)
    objs_ret = repo.bulk_get(media_ids)
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    return Result.ok([SeriesItemDTO(ulid=o.ulid, title=o.title, publish=o.publish) for o in objs])


@Result.shield_exception()
def get_media_series_data(media_type: MediaType, media_id: int) -> Result[MediaSeriesDTO, FatalError]:
    series_ret = get_series_list_data(FilterOption(media_type=media_type, media_ids=[media_id]))
    if series_ret.is_err:
        return Result.err(series_ret.err_value)

    series_list = series_ret.ok_value
    if len(series_list) == 0:
        return Result.ok(MediaSeriesDTO(ulid="", title="", media_ids=[]))

    series = series_list[0]
    return Result.ok(MediaSeriesDTO(ulid=series.ulid, title=series.title, media_ids=series.media_ids))


@Result.shield_exception()
def delete_series_media_data(media_type: MediaType, media_ids: list[int]) -> Result[None, FatalError]:
    if len(media_ids) == 0:
        return Result.ok(None)

    series_ret = get_series_list_data(FilterOption(media_type=media_type, media_ids=media_ids))
    if series_ret.is_err:
        return Result.err(series_ret.err_value)

    series_list = series_ret.ok_value
    delete_set = set(media_ids)
    save_objs = [replace(s, media_ids=[i for i in s.media_ids if i not in delete_set]) for s in series_list]
    repo = injector.get(SeriesInterface)
    save_ret = repo.bulk_save(save_objs)
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(None)


def media_image(media: MediaDataType) -> str:
    return media.image if not isinstance(media, ChatData) else ""


@Result.shield_exception()
def get_published_media_data(media_type: MediaType, media_ids: list[int]) -> Result[list[MediaDataType], FatalError]:
    if len(media_ids) == 0:
        return Result.ok([])

    repo = get_media_repository(media_type)
    ids_ret = repo.get_ids(MediaFilterOption(ids=media_ids, publish=True), MediaSortOption(), MediaPageOption(limit=0))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    id_set = set(ids)
    objs_ret = repo.bulk_get([i for i in media_ids if i in id_set])
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    all_objs = objs_ret.ok_value
    objs: list[MediaDataType] = list(all_objs)
    return Result.ok(objs)
