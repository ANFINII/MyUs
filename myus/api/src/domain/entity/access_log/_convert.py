from api.db.models.common import AccessLog
from api.src.domain.interface.access_log.data import AccessLogData
from api.utils.enum.access_log import AccessType


def convert_data(obj: AccessLog) -> AccessLogData:
    return AccessLogData(
        id=obj.id,
        ip_address=obj.ip_address,
        type=AccessType(obj.type),
        type_id=obj.type_id,
        updated=obj.updated,
    )


def marshal_data(data: AccessLogData) -> AccessLog:
    return AccessLog(
        id=data.id if data.id != 0 else None,
        ip_address=data.ip_address,
        type=data.type.value,
        type_id=data.type_id,
        updated=data.updated,
    )
