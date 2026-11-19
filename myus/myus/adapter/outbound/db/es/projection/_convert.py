from myus.db.models.es import EsProjectionProgress
from myus.domain.es.projection.data import ProjectionProgressData
from myus.utils.enum.es import ProjectorName


def convert_data(obj: EsProjectionProgress) -> ProjectionProgressData:
    return ProjectionProgressData(
        id=obj.id,
        projector=ProjectorName(obj.projector),
        aggregate_type=obj.aggregate_type,
        aggregate_id=obj.aggregate_id,
        last_applied_seq=obj.last_applied_seq,
    )


def marshal_data(data: ProjectionProgressData) -> EsProjectionProgress:
    return EsProjectionProgress(
        id=data.id if data.id != 0 else None,
        projector=data.projector,
        aggregate_type=data.aggregate_type,
        aggregate_id=data.aggregate_id,
        last_applied_seq=data.last_applied_seq,
    )
