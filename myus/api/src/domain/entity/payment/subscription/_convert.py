from api.db.models.payment import Subscription
from api.src.domain.interface.payment.data import Money
from api.src.domain.interface.payment.subscription.data import SubscriptionData
from api.utils.enum.i18n import Currency
from api.utils.enum.payment import PaymentProvider, SubscriptionStatus


def convert_data(obj: Subscription) -> SubscriptionData:
    return SubscriptionData(
        id=obj.id,
        customer_user_id=obj.customer_id,
        seller_id=obj.seller_id,
        provider=PaymentProvider(obj.provider),
        external_id=obj.external_id,
        product_code=obj.product_code,
        price=Money(amount=obj.price_amount, currency=Currency(obj.price_currency)),
        status=SubscriptionStatus(obj.status),
        started_at=obj.started_at,
        current_period_end=obj.current_period_end,
        canceled_at=obj.canceled_at,
    )


def marshal_data(data: SubscriptionData) -> Subscription:
    return Subscription(
        id=data.id if data.id != 0 else None,
        customer_id=data.customer_user_id,
        seller_id=data.seller_id,
        provider=data.provider,
        external_id=data.external_id,
        product_code=data.product_code,
        price_amount=data.price.amount,
        price_currency=data.price.currency,
        status=data.status,
        started_at=data.started_at,
        current_period_end=data.current_period_end,
        canceled_at=data.canceled_at,
    )
