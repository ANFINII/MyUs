from myus.db.models.media import EncodeJob
from myus.domain.encode_job.data import EncodeJobData


def convert_data(obj: EncodeJob) -> EncodeJobData:
    return EncodeJobData(
        id=obj.id,
        video_id=obj.video_id,
        publish=obj.publish,
        processed_at=obj.processed_at,
        attempts=obj.attempts,
        last_error=obj.last_error,
        created=obj.created,
    )


def marshal_data(data: EncodeJobData) -> EncodeJob:
    return EncodeJob(
        id=data.id if data.id != 0 else None,
        video_id=data.video_id,
        publish=data.publish,
        processed_at=data.processed_at,
        attempts=data.attempts,
        last_error=data.last_error,
    )
