from dataclasses import dataclass
from datetime import datetime
from api.utils.enum.media import MediaType


@dataclass(frozen=True, slots=True)
class AccessLogData:
    id: int
    ip_address: str
    type: MediaType
    type_id: int
    updated: datetime
