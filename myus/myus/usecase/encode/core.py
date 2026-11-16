from myus.domain.media.common import FilterOption, PageOption, SortOption
from myus.domain.media.video.interface import VideoInterface
from myus.injectors.container import injector
from myus.utils.common.logger import log
from myus.utils.common.result import FatalError, Result
from myus.utils.enum.media import EncodeStatus
from myus.utils.functions.convert.video_encoding import VideoConvert, convert_video
from myus.utils.functions.transaction import atomic_result
from ._convert import save_encode_failed_data, save_encoded_video_data


ENCODE_RETRY_COUNT = 3


@Result.shield_exception()
def encode_videos(limit: int) -> Result[int, FatalError]:
    repo = injector.get(VideoInterface)
    ids_ret = repo.get_ids(FilterOption(encode_status=EncodeStatus.ENCODING), SortOption(is_asc=True), PageOption(limit=limit))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    videos_ret = repo.bulk_get(ids_ret.ok_value)
    if videos_ret.is_err:
        return Result.err(videos_ret.err_value)

    encoded_count = 0
    for video in videos_ret.ok_value:
        result = VideoConvert(video="", convert="")
        for attempt in range(1, ENCODE_RETRY_COUNT + 1):
            result = convert_video(video.video)
            if result.video != "":
                break
            log.warning("encode failed", video_id=video.id, attempt=attempt)

        if result.video == "":
            log.error("gave up", video_id=video.id, attempts=ENCODE_RETRY_COUNT)
            failed_ret = save_encode_failed_data(video.id)
            if failed_ret.is_err:
                return Result.err(failed_ret.err_value)
            continue

        save_ret = atomic_result(lambda: save_encoded_video_data(video.id, result))
        if save_ret.is_err:
            return Result.err(save_ret.err_value)
        encoded_count += 1

    return Result.ok(encoded_count)
