import json
from dataclasses import asdict, replace
from datetime import datetime, timezone
from api.modules.logger import log
from api.src.domain.interface.payment.subscription.interface import FilterOption as SubscriptionFilterOption, SortOption as SubscriptionSortOption, SubscriptionInterface
from api.src.domain.interface.payment.transaction.interface import FilterOption as TransactionFilterOption, SortOption as TransactionSortOption, TransactionInterface
from api.src.domain.interface.webhook.inbox.data import WebhookInboxData
from api.src.domain.interface.webhook.outbox.data import WebhookOutboxData
from api.src.domain.interface.webhook.outbox.interface import WebhookOutboxInterface
from api.src.injectors.container import injector
from api.src.types.dto.webhook import WebhookOutboxPayloadDTO
from api.utils.enum.payment import PaymentStatus, SubscriptionStatus, WebhookEventType, WebhookDeliveryStatus


def dispatch_webhook_inbox(event: WebhookInboxData) -> None:
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
            log.info("WebhookInbox SUBSCRIPTION_CREATED noop", external_id=event.external_id)
        case WebhookEventType.SUBSCRIPTION_UPDATED:
            log.info("WebhookInbox SUBSCRIPTION_UPDATED noop", external_id=event.external_id)


def enqueue_webhook_outbox(event: WebhookInboxData) -> None:
    repo = injector.get(WebhookOutboxInterface)

    payload = WebhookOutboxPayloadDTO(
        provider=event.provider.value,
        event_id=event.event_id,
        event_type=event.event_type.value,
        external_id=event.external_id,
        occurred_at=event.occurred_at.isoformat(),
    )

    data = WebhookOutboxData(
        id=0,
        provider=event.provider,
        event_type=event.event_type,
        external_id=event.external_id,
        payload=json.dumps(asdict(payload)),
        status=WebhookDeliveryStatus.PENDING,
        occurred_at=event.occurred_at,
        delivered_at=datetime.min.replace(tzinfo=timezone.utc),
    )

    repo.bulk_save([data])
    log.info("WebhookOutbox enqueued", event_id=event.event_id, event_type=event.event_type.value)


def update_subscription_canceled(event: WebhookInboxData) -> None:
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


def update_transaction_status(event: WebhookInboxData, status: PaymentStatus, update_paid_at: bool) -> None:
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
