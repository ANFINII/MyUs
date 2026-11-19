from dataclasses import dataclass
from myus.utils.enum.es import ProjectorName


@dataclass(frozen=True, slots=True)
class ProjectionProgressData:
    id: int
    projector: ProjectorName
    aggregate_type: str
    aggregate_id: str
    last_applied_seq: int
