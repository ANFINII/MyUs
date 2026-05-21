from dataclasses import replace
from api.modules.logger import log
from api.src.domain.interface.payment.subscription.interface import FilterOption as SubscriptionFilterOption, SortOption as SubscriptionSortOption, SubscriptionInterface
from api.src.domain.interface.payment.transaction.interface import FilterOption as TransactionFilterOption, SortOption as TransactionSortOption, TransactionInterface
from api.src.domain.interface.payment.webhook_event.data import WebhookEventData
from api.src.injectors.container import injector
from api.utils.enum.payment import PaymentStatus, SubscriptionStatus, WebhookEventType


def handle_webhook_event(event: WebhookEventData) -> None:
    match event.event_type:
        case WebhookEventType.SUBSCRIPTION_CANCELED:
            update_subscription_canceled(event)
        case WebhookEventType.PAYMENT_SUCCEEDED:
            update_transaction_status(event, PaymentStatus.CAPTURED, update_paid_at=True)
        case WebhookEventType.PAYMENT_FAILED:
            update_transaction_status(event, PaymentStatus.FAILED, update_paid_at=False)
        case WebhookEventType.REFUND_ISSUED:
            update_transaction_status(event, PaymentStatus.REFUNDED, update_paid_at=False)
        case WebhookEventType.SUBSCRIPTION_CREATED:
            log.info("WebhookEvent SUBSCRIPTION_CREATED noop", external_id=event.external_id)
        case WebhookEventType.SUBSCRIPTION_UPDATED:
            log.info("WebhookEvent SUBSCRIPTION_UPDATED noop", external_id=event.external_id)


def update_subscription_canceled(event: WebhookEventData) -> None:
    repo = injector.get(SubscriptionInterface)
    ids = repo.get_ids(
        SubscriptionFilterOption(provider=event.provider.value, external_id=event.external_id),
        SubscriptionSortOption(),
        limit=1,
    )
    if len(ids) == 0:
        log.warning("Subscription not found for cancel", external_id=event.external_id)
        return

    subs = repo.bulk_get(ids)
    updated = replace(subs[0], status=SubscriptionStatus.CANCELED, canceled_at=event.occurred_at)
    repo.bulk_save([updated])
    log.info("Subscription canceled", external_id=event.external_id)


def update_transaction_status(event: WebhookEventData, status: PaymentStatus, update_paid_at: bool) -> None:
    repo = injector.get(TransactionInterface)
    ids = repo.get_ids(
        TransactionFilterOption(provider=event.provider.value, external_id=event.external_id),
        TransactionSortOption(),
        limit=1,
    )
    if len(ids) == 0:
        log.warning("Transaction not found for status update", external_id=event.external_id, status=status.value)
        return

    transactions = repo.bulk_get(ids)
    transaction = transactions[0]
    updated = replace(transaction, status=status, paid_at=event.occurred_at) if update_paid_at else replace(transaction, status=status)
    repo.bulk_save([updated])
    log.info("Transaction status updated", external_id=event.external_id, status=status.value)
