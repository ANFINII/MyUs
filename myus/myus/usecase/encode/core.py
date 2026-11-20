from myus.domain.media.audio.interface import AudioInterface
from myus.domain.media.common import FilterOption, PageOption, SortOption
from myus.domain.media.video.interface import VideoInterface
from myus.injectors.container import injector
from myus.utils.common.logger import log
from myus.utils.common.result import FatalError, Result
from myus.utils.enum.media import EncodeStatus
from myus.utils.functions.convert.audio_converter import AudioConvert, convert_audio, delete_audio
from myus.utils.functions.convert.video_encoding import VideoConvert, convert_video
from myus.utils.functions.transaction import atomic_result
from ._convert import save_encode_failed_data, save_encoded_video_data, save_audio_encode_failed_data, save_encoded_audio_data


ENCODE_RETRY_COUNT = 3


@Result.shield_exception()
def encode_videos(limit: int) -> Result[int, FatalError]:
    repo = injector.get(VideoInterface)
    ids_ret = repo.get_ids(FilterOption(encode_status=EncodeStatus.ENCODING), SortOption(is_asc=True), PageOption(limit=limit))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    videos_ret = repo.bulk_get(ids)
    if videos_ret.is_err:
        return Result.err(videos_ret.err_value)

    videos = videos_ret.ok_value
    encoded_count = 0
    for video in videos:
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


@Result.shield_exception()
def encode_audios(limit: int) -> Result[int, FatalError]:
    repo = injector.get(AudioInterface)
    ids_ret = repo.get_ids(FilterOption(encode_status=EncodeStatus.ENCODING), SortOption(is_asc=True), PageOption(limit=limit))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    audios_ret = repo.bulk_get(ids)
    if audios_ret.is_err:
        return Result.err(audios_ret.err_value)

    audios = audios_ret.ok_value
    encoded_count = 0
    for audio in audios:
        result = AudioConvert(audio="", gain=0.0, is_low_bit_rate=False)
        for attempt in range(1, ENCODE_RETRY_COUNT + 1):
            result = convert_audio(audio.audio)
            if result.audio != "" or result.is_low_bit_rate:
                break
            log.warning("encode failed", audio_id=audio.id, attempt=attempt)

        if result.is_low_bit_rate:
            low_bit_rate_ret = save_audio_encode_failed_data(audio.id, EncodeStatus.LOW_BIT_RATE)
            if low_bit_rate_ret.is_err:
                return Result.err(low_bit_rate_ret.err_value)
            continue

        if result.audio == "":
            log.error("gave up", audio_id=audio.id, attempts=ENCODE_RETRY_COUNT)
            failed_ret = save_audio_encode_failed_data(audio.id, EncodeStatus.FAILED)
            if failed_ret.is_err:
                return Result.err(failed_ret.err_value)
            continue

        save_ret = atomic_result(lambda: save_encoded_audio_data(audio.id, result))
        if save_ret.is_err:
            return Result.err(save_ret.err_value)

        if result.audio != audio.audio:
            delete_audio(audio.audio)
        encoded_count += 1

    return Result.ok(encoded_count)
