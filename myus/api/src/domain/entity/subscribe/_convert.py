from api.db.models.subscribe import Subscribe
from api.src.domain.interface.subscribe.data import SubscribeData


def convert_data(obj: Subscribe) -> SubscribeData:
    return SubscribeData(
        id=obj.id,
        user_id=obj.user_id,
        channel_id=obj.channel_id,
        is_subscribe=obj.is_subscribe,
    )


def marshal_data(data: SubscribeData) -> Subscribe:
    return Subscribe(
        id=data.id if data.id != 0 else None,
        user_id=data.user_id,
        channel_id=data.channel_id,
        is_subscribe=data.is_subscribe,
    )
