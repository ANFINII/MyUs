from dataclasses import replace
from myus.domain.media.video.interface import VideoInterface
from myus.injectors.container import injector
from myus.utils.common.logger import log
from myus.utils.common.result import FatalError, Result
from myus.utils.enum.notification import NotificationObjectType, NotificationTypeNo
from myus.utils.functions.convert.video_encoding import VideoConvert
from ..notification._convert import create_notification_data


@Result.shield_exception()
def save_encoded_video_data(video_id: int, result: VideoConvert) -> Result[None, FatalError]:
    repo = injector.get(VideoInterface)
    videos_ret = repo.bulk_get([video_id])
    if videos_ret.is_err:
        return Result.err(videos_ret.err_value)

    videos = videos_ret.ok_value
    if len(videos) == 0:
        log.info("not found", video_id=video_id)
        return Result.ok(None)

    video = videos[0]
    save_ret = repo.bulk_save([replace(video, video=result.video, convert=result.convert)])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    if video.publish:
        notification_ret = create_notification_data(video.channel.owner_id, 0, NotificationTypeNo.VIDEO, video.id, NotificationObjectType.VIDEO)
        if notification_ret.is_err:
            log.error("create failed", error=notification_ret.err_value.message, object_type=NotificationObjectType.VIDEO.value, object_id=video.id)

    return Result.ok(None)


@Result.shield_exception()
def save_encode_failed_data(video_id: int) -> Result[None, FatalError]:
    repo = injector.get(VideoInterface)
    videos_ret = repo.bulk_get([video_id])
    if videos_ret.is_err:
        return Result.err(videos_ret.err_value)

    videos = videos_ret.ok_value
    if len(videos) == 0:
        log.info("not found", video_id=video_id)
        return Result.ok(None)

    save_ret = repo.bulk_save([replace(videos[0], encode_failed=True)])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(None)
