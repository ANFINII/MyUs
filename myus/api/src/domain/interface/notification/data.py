from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NotificationData:
    id: int
    user_from_id: int
    user_to_id: int
    type_no: int
    type_name: str
    object_id: int
    object_type: str
