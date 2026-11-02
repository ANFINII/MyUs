from api.db.models.payment import PaymentPayout
from api.src.domain.interface.payment.payout.data import PayoutData
from api.utils.enum.i18n import Currency
from api.utils.enum.payment import PaymentProvider, PayoutStatus


def convert_data(obj: PaymentPayout) -> PayoutData:
    return PayoutData(
        id=obj.id,
        provider=PaymentProvider(obj.provider),
        external_id=obj.external_id,
        amount=obj.amount,
        currency=Currency(obj.currency),
        status=PayoutStatus(obj.status),
        arrival_at=obj.arrival_at,
        last_event_at=obj.last_event_at,
    )


def marshal_data(data: PayoutData) -> PaymentPayout:
    return PaymentPayout(
        id=data.id if data.id != 0 else None,
        provider=data.provider,
        external_id=data.external_id,
        amount=data.amount,
        currency=data.currency,
        status=data.status,
        arrival_at=data.arrival_at,
        last_event_at=data.last_event_at,
    )
