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
from api.utils.common.result import FatalError, Result
from api.utils.enum.payment import PaymentStatus, SubscriptionStatus, WebhookEventType, WebhookDeliveryStatus


@Result.shield_exception()
def dispatch_webhook_inbox(event: WebhookInboxData) -> Result[None, FatalError]:
    match event.event_type:
        case WebhookEventType.SUBSCRIPTION_CANCELED:
            ret = update_subscription_canceled(event)
        case WebhookEventType.PAYMENT_SUCCEEDED:
            ret = update_transaction_status(event, PaymentStatus.CAPTURED, update_paid_at=True)
        case WebhookEventType.PAYMENT_FAILED:
            ret = update_transaction_status(event, PaymentStatus.FAILED, update_paid_at=False)
        case WebhookEventType.REFUND_ISSUED:
            ret = update_transaction_status(event, PaymentStatus.REFUNDED, update_paid_at=False)
        case WebhookEventType.SUBSCRIPTION_CREATED:
            log.info("WebhookInbox SUBSCRIPTION_CREATED noop", external_id=event.external_id)
            return Result.ok(None)
        case WebhookEventType.SUBSCRIPTION_UPDATED:
            log.info("WebhookInbox SUBSCRIPTION_UPDATED noop", external_id=event.external_id)
            return Result.ok(None)

    if ret.is_err:
        return Result.err(ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def enqueue_webhook_outbox(event: WebhookInboxData) -> Result[None, FatalError]:
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

    ret = repo.bulk_save([data])
    if ret.is_err:
        return Result.err(ret.err_value)

    log.info("WebhookOutbox enqueued", event_id=event.event_id, event_type=event.event_type.value)
    return Result.ok(None)


@Result.shield_exception()
def update_subscription_canceled(event: WebhookInboxData) -> Result[None, FatalError]:
    repo = injector.get(SubscriptionInterface)
    ids_ret = repo.get_ids(
        SubscriptionFilterOption(provider=event.provider.value, external_id=event.external_id),
        SubscriptionSortOption(),
        limit=1,
    )
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.warning("Subscription not found for cancel", external_id=event.external_id)
        return Result.ok(None)

    subs_ret = repo.bulk_get(ids)
    if subs_ret.is_err:
        return Result.err(subs_ret.err_value)

    subs = subs_ret.ok_value
    updated = replace(subs[0], status=SubscriptionStatus.CANCELED, canceled_at=event.occurred_at)
    save_ret = repo.bulk_save([updated])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    log.info("Subscription canceled", external_id=event.external_id)
    return Result.ok(None)


@Result.shield_exception()
def update_transaction_status(event: WebhookInboxData, status: PaymentStatus, update_paid_at: bool) -> Result[None, FatalError]:
    repo = injector.get(TransactionInterface)
    ids_ret = repo.get_ids(
        TransactionFilterOption(provider=event.provider.value, external_id=event.external_id),
        TransactionSortOption(),
        limit=1,
    )
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.warning("Transaction not found for status update", external_id=event.external_id, status=status.value)
        return Result.ok(None)

    transactions_ret = repo.bulk_get(ids)
    if transactions_ret.is_err:
        return Result.err(transactions_ret.err_value)

    transactions = transactions_ret.ok_value
    transaction = transactions[0]
    updated = replace(transaction, status=status, paid_at=event.occurred_at) if update_paid_at else replace(transaction, status=status)
    save_ret = repo.bulk_save([updated])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    log.info("Transaction status updated", external_id=event.external_id, status=status.value)
    return Result.ok(None)
