from dataclasses import replace
from datetime import datetime, timezone
from typing import assert_never
from api.modules.logger import log
from api.src.domain.aggregate.subscription.state import ActiveSubscription, EndedSubscription, IncompleteSubscription, PastDueSubscription, SubscriptionState, convert_status
from api.src.domain.interface.payment.customer.data import PaymentCustomerData
from api.src.domain.interface.payment.customer.interface import FilterOption as PaymentCustomerFilterOption, SortOption as PaymentCustomerSortOption, PaymentCustomerInterface
from api.src.domain.interface.payment.event.data import BalanceData, PaymentEventData, PaymentFailedContent, PaymentPaidContent, PayoutContent, ProviderSubscriptionData, RefundContent
from api.src.domain.interface.payment.event.interface import FilterOption as PaymentEventFilterOption, SortOption as PaymentEventSortOption, PaymentEventInterface
from api.src.domain.interface.payment.ledger.data import LedgerEntryData
from api.src.domain.interface.payment.ledger.interface import FilterOption as LedgerEntryFilterOption, SortOption as LedgerEntrySortOption, LedgerEntryInterface
from api.src.domain.interface.payment.payout.data import PayoutData
from api.src.domain.interface.payment.payout.interface import FilterOption as PayoutFilterOption, SortOption as PayoutSortOption, PayoutInterface
from api.src.domain.interface.payment.provider.interface import PaymentInterface
from api.src.domain.interface.payment.subscription.data import SubscriptionData
from api.src.domain.interface.payment.subscription.interface import FilterOption as SubscriptionFilterOption, SortOption as SubscriptionSortOption, SubscriptionInterface
from api.src.domain.interface.payment.transaction.data import TransactionData
from api.src.domain.interface.payment.transaction.interface import FilterOption as TransactionFilterOption, SortOption as TransactionSortOption, TransactionInterface
from api.src.domain.interface.user.data import UserAllData
from api.src.injectors.container import injector
from api.src.usecase.command.subscription import accept_provider_subscription
from api.src.usecase.user.core import get_user_data
from api.src.usecase.user._convert import save_user_data
from api.utils.common.result import CommandError, FatalError, Result
from api.utils.enum.payment import LedgerEntryType, PaymentProvider, PaymentStatus, SubscriptionStatus
from api.utils.enum.user import PlanName
from api.utils.functions.map import payment_status_rank
from api.utils.functions.payment import included_tax
from api.utils.plan import get_plan


TAX_RATE = 10
REPLAY_BATCH_SIZE = 100
PAYMENT_EVENT_MAX_ATTEMPTS = 30


def get_payment_repository(provider: PaymentProvider) -> PaymentInterface:
    providers = injector.get(dict[PaymentProvider, PaymentInterface])
    return providers[provider]


@Result.shield_exception()
def record_payment_event(event: PaymentEventData) -> Result[int | None, FatalError]:
    repo = injector.get(PaymentEventInterface)
    filter = PaymentEventFilterOption(provider=event.provider.value, event_id=event.event_id)
    ids_ret = repo.get_ids(filter, PaymentEventSortOption(), limit=1)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) > 0:
        log.info("PaymentEvent already recorded", event_id=event.event_id)
        return Result.ok(None)

    save_ret = repo.bulk_save([event])
    if save_ret.is_err:
        saved_ids_ret = repo.get_ids(filter, PaymentEventSortOption(), limit=1)
        if saved_ids_ret.is_err:
            return Result.err(saved_ids_ret.err_value)

        saved_ids = saved_ids_ret.ok_value
        if len(saved_ids) > 0:
            log.info("PaymentEvent recorded by another request", event_id=event.event_id)
            return Result.ok(None)

        return Result.err(save_ret.err_value)

    new_ids = save_ret.ok_value
    return Result.ok(new_ids[0])


@Result.shield_exception()
def apply_payment_event(event: PaymentEventData) -> Result[None, CommandError]:
    match event.content:
        case ProviderSubscriptionData() as provider_subscription:
            command_ret = accept_provider_subscription(provider_subscription, event.occurred_at)
            if command_ret.is_err:
                return Result.err(command_ret.err_value)

            state = command_ret.ok_value
            ret = update_subscription(event, state)
        case PaymentPaidContent() as paid:
            ret = record_payment(event, paid)
        case PaymentFailedContent():
            ret = update_transaction_status(event, PaymentStatus.FAILED)
        case RefundContent() as refund:
            ret = record_refund(event, refund)
        case PayoutContent() as payout:
            ret = record_payout(event, payout)
        case _:
            assert_never(event.content)

    if ret.is_err:
        return Result.err(ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def update_subscription(event: PaymentEventData, state: SubscriptionState) -> Result[None, FatalError]:
    detail = state.detail
    if get_plan(detail.product_code) is None:
        log.error("Subscription unknown plan", external_id=event.external_id, product_code=detail.product_code)
        return Result.ok(None)

    if len(detail.user_ulid) == 0:
        log.error("Subscription user_ulid missing", external_id=event.external_id)
        return Result.ok(None)

    user_ret = get_user_data(ulid=detail.user_ulid)
    if user_ret.is_err:
        return Result.err(user_ret.err_value)

    user = user_ret.ok_value
    if user is None:
        log.error("Subscription user not found", external_id=event.external_id, user_ulid=detail.user_ulid)
        return Result.ok(None)

    repo = injector.get(SubscriptionInterface)
    ids_ret = repo.get_ids(SubscriptionFilterOption(provider=detail.provider.value, external_id=detail.external_id), SubscriptionSortOption(), limit=1)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    customer_ret = save_payment_customer_data(user.user.id, detail.provider, detail.customer_id)
    if customer_ret.is_err:
        return Result.err(customer_ret.err_value)

    customer_id = customer_ret.ok_value
    status = convert_status(state)
    subscription = SubscriptionData(
        id=ids[0] if len(ids) > 0 else 0,
        payment_customer_id=customer_id,
        seller_id="",
        external_id=detail.external_id,
        product_code=detail.product_code,
        price=detail.price,
        status=status,
        started_at=detail.started_at,
        current_period_end=detail.current_period_end,
        canceled_at=detail.canceled_at,
        last_event_at=state.last_occurred_at,
    )
    subscription_ret = save_subscription_data(subscription)
    if subscription_ret.is_err:
        return Result.err(subscription_ret.err_value)

    user_plan_ret = update_user_plan(user, state)
    if user_plan_ret.is_err:
        return Result.err(user_plan_ret.err_value)

    log.info("Subscription updated", external_id=event.external_id, status=status.value)
    return Result.ok(None)


@Result.shield_exception()
def update_user_plan(user: UserAllData, state: SubscriptionState) -> Result[None, FatalError]:
    detail = state.detail
    match state:
        case ActiveSubscription() | PastDueSubscription():
            user_plan = replace(
                user.user_plan,
                plan=detail.product_code,
                is_paid=True,
                start_date=detail.started_at,
                end_date=detail.current_period_end,
            )
        case EndedSubscription():
            repo = injector.get(SubscriptionInterface)
            ids_ret = repo.get_ids(SubscriptionFilterOption(customer_user_id=user.user.id), SubscriptionSortOption(), limit=None)
            if ids_ret.is_err:
                return Result.err(ids_ret.err_value)

            ids = ids_ret.ok_value
            subscriptions_ret = repo.bulk_get(ids)
            if subscriptions_ret.is_err:
                return Result.err(subscriptions_ret.err_value)

            subscriptions = subscriptions_ret.ok_value
            active_subscriptions = [s for s in subscriptions if s.status in (SubscriptionStatus.ACTIVE, SubscriptionStatus.PAST_DUE)]
            if len(active_subscriptions) > 0:
                return Result.ok(None)

            user_plan = replace(user.user_plan, plan=PlanName.FREE, is_paid=False, end_date=detail.current_period_end)
        case IncompleteSubscription():
            return Result.ok(None)
        case _:
            assert_never(state)

    ret = save_user_data(replace(user, user_plan=user_plan))
    if ret.is_err:
        return Result.err(ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def record_payment(event: PaymentEventData, paid: PaymentPaidContent) -> Result[None, FatalError]:
    user_ret = get_user_data(ulid=paid.user_ulid)
    if user_ret.is_err:
        return Result.err(user_ret.err_value)

    user = user_ret.ok_value
    if user is None:
        log.error("Payment user not found", external_id=event.external_id, user_ulid=paid.user_ulid)
        return Result.err(FatalError("Payment user not found"))

    customer_ret = save_payment_customer_data(user.user.id, event.provider, paid.customer_id)
    if customer_ret.is_err:
        return Result.err(customer_ret.err_value)

    customer_id = customer_ret.ok_value
    subscription_id = 0
    if len(paid.subscription_external_id) > 0:
        subscription_repo = injector.get(SubscriptionInterface)
        subscription_ids_ret = subscription_repo.get_ids(SubscriptionFilterOption(provider=event.provider.value, external_id=paid.subscription_external_id), SubscriptionSortOption(), limit=1)
        if subscription_ids_ret.is_err:
            return Result.err(subscription_ids_ret.err_value)

        subscription_ids = subscription_ids_ret.ok_value
        if len(subscription_ids) == 0:
            log.warning("Payment subscription not yet recorded", external_id=event.external_id, subscription=paid.subscription_external_id)
            return Result.err(FatalError("Payment subscription not yet recorded"))

        subscription_id = subscription_ids[0]

    transaction_ret = get_transaction_data(event)
    if transaction_ret.is_err:
        return Result.err(transaction_ret.err_value)

    payment_transaction = transaction_ret.ok_value
    if payment_transaction is None or payment_transaction.last_event_at <= event.occurred_at:
        status = PaymentStatus.CAPTURED
        if payment_transaction is not None and payment_status_rank(payment_transaction.status) > payment_status_rank(status):
            status = payment_transaction.status

        transaction = TransactionData(
            id=payment_transaction.id if payment_transaction is not None else 0,
            payment_customer_id=customer_id,
            subscription_id=subscription_id,
            external_id=event.external_id,
            currency=paid.balance.currency,
            tax_rate=TAX_RATE,
            receipt_number=paid.receipt_number,
            status=status,
            paid_at=paid.balance.occurred_at,
            last_event_at=event.occurred_at,
        )
        save_ret = save_transaction_data(transaction)
        if save_ret.is_err:
            return Result.err(save_ret.err_value)

        payment_transaction = replace(transaction, id=save_ret.ok_value)

    ledger_ret = save_ledger_entry_data(payment_transaction.id, event.id, LedgerEntryType.SALE, [paid.balance])
    if ledger_ret.is_err:
        return Result.err(ledger_ret.err_value)

    log.info("Payment recorded", external_id=event.external_id, amount=paid.balance.amount)
    return Result.ok(None)


@Result.shield_exception()
def record_refund(event: PaymentEventData, refund: RefundContent) -> Result[None, FatalError]:
    transaction_ret = get_transaction_data(event)
    if transaction_ret.is_err:
        return Result.err(transaction_ret.err_value)

    payment_transaction = transaction_ret.ok_value
    if payment_transaction is None:
        log.warning("Refund transaction not yet recorded", external_id=event.external_id)
        return Result.err(FatalError("Refund transaction not yet recorded"))

    ledger_ret = save_ledger_entry_data(payment_transaction.id, event.id, LedgerEntryType.REFUND, refund.balances)
    if ledger_ret.is_err:
        return Result.err(ledger_ret.err_value)

    status_ret = update_transaction_status(event, PaymentStatus.REFUNDED)
    if status_ret.is_err:
        return Result.err(status_ret.err_value)

    log.info("Refund recorded", external_id=event.external_id)
    return Result.ok(None)


@Result.shield_exception()
def record_payout(event: PaymentEventData, payout: PayoutContent) -> Result[None, FatalError]:
    repo = injector.get(PayoutInterface)
    ids_ret = repo.get_ids(PayoutFilterOption(provider=event.provider.value, external_id=event.external_id), PayoutSortOption(), limit=1)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    payouts_ret = repo.bulk_get(ids)
    if payouts_ret.is_err:
        return Result.err(payouts_ret.err_value)

    payouts = payouts_ret.ok_value
    if len(payouts) > 0 and payouts[0].last_event_at > event.occurred_at:
        log.info("Payout event is older than applied", external_id=event.external_id, event_id=event.event_id)
        return Result.ok(None)

    data = PayoutData(
        id=ids[0] if len(ids) > 0 else 0,
        provider=event.provider,
        external_id=event.external_id,
        amount=payout.amount,
        currency=payout.currency,
        status=payout.status,
        arrival_at=payout.arrival_at,
        last_event_at=event.occurred_at,
    )
    save_ret = repo.bulk_save([data])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    new_ids = save_ret.ok_value
    payout_id = ids[0] if len(ids) > 0 else new_ids[0]

    ledger_repo = injector.get(LedgerEntryInterface)
    entry_ids_ret = ledger_repo.get_ids(LedgerEntryFilterOption(external_ids=payout.balance_external_ids), LedgerEntrySortOption(), limit=None)
    if entry_ids_ret.is_err:
        return Result.err(entry_ids_ret.err_value)

    entry_ids = entry_ids_ret.ok_value
    entries_ret = ledger_repo.bulk_get(entry_ids)
    if entries_ret.is_err:
        return Result.err(entries_ret.err_value)

    entries = entries_ret.ok_value
    entries_save_ret = ledger_repo.bulk_save([replace(e, payout_id=payout_id) for e in entries])
    if entries_save_ret.is_err:
        return Result.err(entries_save_ret.err_value)

    log.info("Payout recorded", external_id=event.external_id, amount=payout.amount, entries=len(entries))
    return Result.ok(None)


@Result.shield_exception()
def get_transaction_data(event: PaymentEventData) -> Result[TransactionData | None, FatalError]:
    repo = injector.get(TransactionInterface)
    ids_ret = repo.get_ids(TransactionFilterOption(provider=event.provider.value, external_id=event.external_id), TransactionSortOption(), limit=1)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    transactions_ret = repo.bulk_get(ids)
    if transactions_ret.is_err:
        return Result.err(transactions_ret.err_value)

    transactions = transactions_ret.ok_value
    if len(transactions) == 0:
        return Result.ok(None)

    return Result.ok(transactions[0])


@Result.shield_exception()
def update_transaction_status(event: PaymentEventData, status: PaymentStatus) -> Result[None, FatalError]:
    transaction_ret = get_transaction_data(event)
    if transaction_ret.is_err:
        return Result.err(transaction_ret.err_value)

    payment_transaction = transaction_ret.ok_value
    if payment_transaction is None:
        log.warning("Transaction not found for status update", external_id=event.external_id, status=status.value)
        return Result.ok(None)

    if payment_status_rank(status) < payment_status_rank(payment_transaction.status):
        log.info("Transaction status not downgraded", external_id=event.external_id, current=payment_transaction.status.value, status=status.value)
        return Result.ok(None)

    if payment_transaction.last_event_at > event.occurred_at:
        log.info("Transaction event is older than applied", external_id=event.external_id, event_id=event.event_id)
        return Result.ok(None)

    save_ret = save_transaction_data(replace(payment_transaction, status=status, last_event_at=event.occurred_at))
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    log.info("Transaction status updated", external_id=event.external_id, status=status.value)
    return Result.ok(None)


@Result.shield_exception()
def save_processed_payment_event_data(event: PaymentEventData) -> Result[None, CommandError]:
    apply_ret = apply_payment_event(event)
    if apply_ret.is_err:
        return Result.err(apply_ret.err_value)

    repo = injector.get(PaymentEventInterface)
    save_ret = repo.bulk_save([replace(event, processed_at=datetime.now(timezone.utc), last_error="")])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def save_failed_payment_event_data(event: PaymentEventData, error: str) -> Result[None, FatalError]:
    attempts = event.attempts + 1
    repo = injector.get(PaymentEventInterface)
    save_ret = repo.bulk_save([replace(event, attempts=attempts, last_error=error)])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    if attempts >= PAYMENT_EVENT_MAX_ATTEMPTS:
        log.error("PaymentEvent gave up", event_id=event.event_id, event_type=event.event_type.value, attempts=attempts, error=error)
    else:
        log.warning("PaymentEvent process failed", event_id=event.event_id, event_type=event.event_type.value, attempts=attempts, error=error)
    return Result.ok(None)


@Result.shield_exception()
def save_payment_customer_data(user_id: int, provider: PaymentProvider, external_id: str) -> Result[int, FatalError]:
    repo = injector.get(PaymentCustomerInterface)
    ids_ret = repo.get_ids(PaymentCustomerFilterOption(user_id=user_id, provider=provider.value), PaymentCustomerSortOption(), limit=1)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) > 0:
        return Result.ok(ids[0])

    save_ret = repo.bulk_save([PaymentCustomerData(id=0, user_id=user_id, provider=provider, external_id=external_id)])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    new_ids = save_ret.ok_value
    return Result.ok(new_ids[0])


@Result.shield_exception()
def save_subscription_data(data: SubscriptionData) -> Result[None, FatalError]:
    repo = injector.get(SubscriptionInterface)
    ret = repo.bulk_save([data])
    if ret.is_err:
        return Result.err(ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def save_transaction_data(data: TransactionData) -> Result[int, FatalError]:
    repo = injector.get(TransactionInterface)
    ret = repo.bulk_save([data])
    if ret.is_err:
        return Result.err(ret.err_value)

    new_ids = ret.ok_value
    return Result.ok(data.id if data.id != 0 else new_ids[0])


@Result.shield_exception()
def save_ledger_entry_data(transaction_id: int, event_id: int, entry_type: LedgerEntryType, balances: list[BalanceData]) -> Result[None, FatalError]:
    repo = injector.get(LedgerEntryInterface)
    external_ids = [b.external_id for b in balances]
    ids_ret = repo.get_ids(LedgerEntryFilterOption(transaction_id=transaction_id, external_ids=external_ids), LedgerEntrySortOption(), limit=None)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    entries_ret = repo.bulk_get(ids)
    if entries_ret.is_err:
        return Result.err(entries_ret.err_value)

    entries = entries_ret.ok_value
    recorded = {(e.external_id, e.entry_type) for e in entries}
    new_entries: list[LedgerEntryData] = []
    for balance in balances:
        if (balance.external_id, entry_type) not in recorded:
            new_entries.append(LedgerEntryData(
                id=0,
                transaction_id=transaction_id,
                payout_id=0,
                event_id=event_id,
                external_id=balance.external_id,
                entry_type=entry_type,
                amount=balance.amount,
                tax_amount=included_tax(balance.amount, TAX_RATE),
                occurred_at=balance.occurred_at,
            ))
        if balance.fee != 0 and (balance.external_id, LedgerEntryType.FEE) not in recorded:
            new_entries.append(LedgerEntryData(
                id=0,
                transaction_id=transaction_id,
                payout_id=0,
                event_id=event_id,
                external_id=balance.external_id,
                entry_type=LedgerEntryType.FEE,
                amount=-balance.fee,
                tax_amount=0,
                occurred_at=balance.occurred_at,
            ))

    save_ret = repo.bulk_save(new_entries)
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(None)


@Result.shield_exception()
def save_payment_projection_data() -> Result[int, CommandError]:
    delete_ret = delete_payment_projection_data()
    if delete_ret.is_err:
        return Result.err(delete_ret.err_value)

    repo = injector.get(PaymentEventInterface)
    ids_ret = repo.get_ids(PaymentEventFilterOption(is_processed=True), PaymentEventSortOption(), limit=None)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    for start in range(0, len(ids), REPLAY_BATCH_SIZE):
        events_ret = repo.bulk_get(ids[start:start + REPLAY_BATCH_SIZE])
        if events_ret.is_err:
            return Result.err(events_ret.err_value)

        events = events_ret.ok_value
        for event in events:
            apply_ret = apply_payment_event(event)
            if apply_ret.is_err:
                log.error("PaymentEvent replay failed", event_id=event.event_id, error=apply_ret.err_value.message)
                return Result.err(apply_ret.err_value)

    log.info("PaymentEvent replayed", count=len(ids))
    return Result.ok(len(ids))


@Result.shield_exception()
def delete_payment_projection_data() -> Result[None, FatalError]:
    ledger_repo = injector.get(LedgerEntryInterface)
    ledger_ids_ret = ledger_repo.get_ids(LedgerEntryFilterOption(), LedgerEntrySortOption(), limit=None)
    if ledger_ids_ret.is_err:
        return Result.err(ledger_ids_ret.err_value)

    ledger_ids = ledger_ids_ret.ok_value
    ledger_ret = ledger_repo.bulk_delete(ledger_ids)
    if ledger_ret.is_err:
        return Result.err(ledger_ret.err_value)

    payout_repo = injector.get(PayoutInterface)
    payout_ids_ret = payout_repo.get_ids(PayoutFilterOption(), PayoutSortOption(), limit=None)
    if payout_ids_ret.is_err:
        return Result.err(payout_ids_ret.err_value)

    payout_ids = payout_ids_ret.ok_value
    payout_ret = payout_repo.bulk_delete(payout_ids)
    if payout_ret.is_err:
        return Result.err(payout_ret.err_value)

    transaction_repo = injector.get(TransactionInterface)
    transaction_ids_ret = transaction_repo.get_ids(TransactionFilterOption(), TransactionSortOption(), limit=None)
    if transaction_ids_ret.is_err:
        return Result.err(transaction_ids_ret.err_value)

    transaction_ids = transaction_ids_ret.ok_value
    transaction_ret = transaction_repo.bulk_delete(transaction_ids)
    if transaction_ret.is_err:
        return Result.err(transaction_ret.err_value)

    subscription_repo = injector.get(SubscriptionInterface)
    subscription_ids_ret = subscription_repo.get_ids(SubscriptionFilterOption(), SubscriptionSortOption(), limit=None)
    if subscription_ids_ret.is_err:
        return Result.err(subscription_ids_ret.err_value)

    subscription_ids = subscription_ids_ret.ok_value
    subscription_ret = subscription_repo.bulk_delete(subscription_ids)
    if subscription_ret.is_err:
        return Result.err(subscription_ret.err_value)

    return Result.ok(None)
