from api.db.models.es import EsSubscriptionLookup
from api.src.domain.interface.es.subscription_lookup.data import SubscriptionLookupData
from api.utils.enum.payment import PaymentProvider


def convert_data(obj: EsSubscriptionLookup) -> SubscriptionLookupData:
    return SubscriptionLookupData(
        id=obj.id,
        aggregate_id=obj.aggregate_id,
        provider=PaymentProvider(obj.provider),
        external_id=obj.external_id,
    )


def marshal_data(data: SubscriptionLookupData) -> EsSubscriptionLookup:
    return EsSubscriptionLookup(
        id=data.id if data.id != 0 else None,
        aggregate_id=data.aggregate_id,
        provider=data.provider,
        external_id=data.external_id,
    )
