from uuid import UUID, uuid5


EVENT_ID_NAMESPACE = UUID("6f1c2a52-5d0e-4c55-9a7e-3b8f1e2d4c60")


def new_event_id(aggregate_type: str, aggregate_id: str, seq: int) -> UUID:
    return uuid5(EVENT_ID_NAMESPACE, f"{aggregate_type}:{aggregate_id}:{seq}")
