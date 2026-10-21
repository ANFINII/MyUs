from dataclasses import dataclass
from datetime import datetime
from api.utils.enum.access_log import AccessType


@dataclass(frozen=True, slots=True)
class AccessLogData:
    id: int
    ip_address: str
    type: AccessType
    type_id: int
    updated: datetime
