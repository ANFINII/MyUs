from dataclasses import replace
from datetime import UTC, datetime
from myus.domain.encode_job.data import EncodeJobData
from myus.domain.encode_job.interface import EncodeJobInterface
from myus.domain.media.video.interface import VideoInterface
from myus.injectors.container import injector
from myus.utils.common.logger import log
from myus.utils.common.result import FatalError, Result
from myus.utils.enum.notification import NotificationObjectType, NotificationTypeNo
from myus.utils.functions.convert.video_encoding import VideoConvert, convert_video
from myus.utils.functions.transaction import atomic_result
from ..notification._convert import create_notification_data


ENCODE_JOB_MAX_ATTEMPTS = 3


@Result.shield_exception()
def save_processed_encode_job_data(job: EncodeJobData) -> Result[None, FatalError]:
    video_repo = injector.get(VideoInterface)
    videos_ret = video_repo.bulk_get([job.video_id])
    if videos_ret.is_err:
        return Result.err(videos_ret.err_value)

    videos = videos_ret.ok_value
    if len(videos) == 0:
        log.error("not found", video_id=job.video_id)
        return Result.err(FatalError("video not found"))

    result = convert_video(videos[0].video)
    if result.video == "":
        return Result.err(FatalError("encode failed"))

    return atomic_result(lambda: save_encoded_video_data(job, result))


@Result.shield_exception()
def save_encoded_video_data(job: EncodeJobData, result: VideoConvert) -> Result[None, FatalError]:
    video_repo = injector.get(VideoInterface)
    videos_ret = video_repo.bulk_get([job.video_id])
    if videos_ret.is_err:
        return Result.err(videos_ret.err_value)

    videos = videos_ret.ok_value
    if len(videos) == 0:
        log.error("not found", video_id=job.video_id)
        return Result.err(FatalError("video not found"))

    video = videos[0]
    publish = job.publish if video.updated <= job.created else video.publish
    save_ret = video_repo.bulk_save([replace(video, video=result.video, convert=result.convert, publish=publish)])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    repo = injector.get(EncodeJobInterface)
    job_ret = repo.bulk_save([replace(job, processed_at=datetime.now(UTC), last_error="")])
    if job_ret.is_err:
        return Result.err(job_ret.err_value)

    if publish:
        notification_ret = create_notification_data(video.channel.owner_id, 0, NotificationTypeNo.VIDEO, video.id, NotificationObjectType.VIDEO)
        if notification_ret.is_err:
            log.error("create failed", error=notification_ret.err_value.message, object_type=NotificationObjectType.VIDEO.value, object_id=video.id)

    return Result.ok(None)


@Result.shield_exception()
def save_failed_encode_job_data(job: EncodeJobData, error: str) -> Result[None, FatalError]:
    attempts = job.attempts + 1
    repo = injector.get(EncodeJobInterface)
    save_ret = repo.bulk_save([replace(job, attempts=attempts, last_error=error)])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    if attempts >= ENCODE_JOB_MAX_ATTEMPTS:
        log.error("gave up", video_id=job.video_id, attempts=attempts, error=error)
    else:
        log.warning("process failed", video_id=job.video_id, attempts=attempts, error=error)
    return Result.ok(None)
