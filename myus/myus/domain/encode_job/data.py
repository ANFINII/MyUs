from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class EncodeJobData:
    id: int
    video_id: int
    publish: bool
    processed_at: datetime
    attempts: int
    last_error: str
    created: datetime
