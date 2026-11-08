from dataclasses import replace
from datetime import datetime, timezone
from typing import assert_never
from django.conf import settings
from api.modules.logger import log
from api.src.domain.interface.payment.customer.interface import PaymentCustomerInterface
from api.src.domain.interface.payment.data import Money
from api.src.domain.interface.payment.event.data import PaymentEventData
from api.src.domain.interface.payment.event.interface import FilterOption as PaymentEventFilterOption, SortOption as PaymentEventSortOption, PaymentEventInterface
from api.src.domain.interface.payment.ledger.interface import FilterOption as LedgerEntryFilterOption, SortOption as LedgerEntrySortOption, LedgerEntryInterface
from api.src.domain.interface.payment.payout.interface import PayoutInterface
from api.src.domain.interface.payment.provider.data import CancelResult, CancelSuccess, CancelFailed, CheckoutData, CheckoutResult, CustomerData, MarketplaceData, RedirectUrls, WebhookVerifyResult
from api.src.domain.interface.payment.subscription.interface import FilterOption as SubscriptionFilterOption, SortOption as SubscriptionSortOption, SubscriptionInterface
from api.src.domain.interface.payment.transaction.interface import TransactionInterface
from api.src.injectors.container import injector
from api.src.types.dto.ledger import LedgerRowDTO
from api.src.usecase.user.core import get_user_data
from api.src.usecase.payment._convert import get_payment_repository, save_payment_event_data, save_provider_subscription_data, save_cancellation_request_data, save_cancellation_failure_data, save_processed_payment_event_data, save_failed_payment_event_data, save_payment_projection_data, PAYMENT_EVENT_MAX_ATTEMPTS
from api.utils.common.result import CommandError, ConflictError, FatalError, FindError, HistoryCorruptedError, InputError, NotFoundError, Result, ValidationError
from api.utils.enum.i18n import Currency, Locale
from api.utils.enum.payment import CancelError, PaymentProvider, PaymentType, SubscriptionStatus
from api.utils.functions.map import locale_path
from api.utils.functions.transaction import atomic_result
from api.utils.plan import get_plan


CHECKOUT_PROVIDER = PaymentProvider.STRIPE


@Result.shield_exception()
def create_checkout(user_id: int, plan_name: str, locale: Locale) -> Result[CheckoutResult, InputError]:
    user_ret = get_user_data(user_id=user_id)
    if user_ret.is_err:
        return Result.err(user_ret.err_value)

    user = user_ret.ok_value
    if user is None:
        return Result.err(NotFoundError("Not Found"))

    plan = get_plan(plan_name)
    if plan is None:
        log.warning("Payment unknown plan", plan=plan_name)
        return Result.err(NotFoundError("Not Found"))

    subscription_repo = injector.get(SubscriptionInterface)
    subscription_ids_ret = subscription_repo.get_ids(SubscriptionFilterOption(customer_user_id=user_id), SubscriptionSortOption(), limit=None)
    if subscription_ids_ret.is_err:
        return Result.err(subscription_ids_ret.err_value)

    subscription_ids = subscription_ids_ret.ok_value
    subscriptions_ret = subscription_repo.bulk_get(subscription_ids)
    if subscriptions_ret.is_err:
        return Result.err(subscriptions_ret.err_value)

    subscriptions = subscriptions_ret.ok_value
    if any(s.status in (SubscriptionStatus.ACTIVE, SubscriptionStatus.PAST_DUE) for s in subscriptions):
        log.warning("Payment checkout already subscribed", user_id=user_id, plan=plan_name)
        return Result.err(ValidationError("error.alreadySubscribed"))

    frontend_url = f"{settings.FRONTEND_URL}{locale_path(locale)}"
    data = CheckoutData(
        product_code=plan.name,
        description=plan.description,
        price=Money(amount=plan.price, currency=Currency.JPY),
        payment_type=PaymentType.SUBSCRIPTION,
        customer=CustomerData(user_ulid=user.user.ulid, email=user.user.email),
        redirect=RedirectUrls(
            success_url=f"{frontend_url}/setting/payment/success",
            cancel_url=f"{frontend_url}/setting/payment/cancel",
        ),
        marketplace=MarketplaceData(seller_id="", application_fee=Money(amount=0, currency=Currency.JPY)),
        locale=locale,
    )

    repo = get_payment_repository(CHECKOUT_PROVIDER)
    checkout_ret = repo.create_checkout(data)
    if checkout_ret.is_err:
        return Result.err(checkout_ret.err_value)

    checkout = checkout_ret.ok_value
    return Result.ok(checkout)


@Result.shield_exception()
def verify_webhook(provider: PaymentProvider, payload: bytes, signature: str) -> Result[WebhookVerifyResult, FatalError]:
    repo = get_payment_repository(provider)
    ret = repo.verify_webhook(payload, signature)
    if ret.is_err:
        return Result.err(ret.err_value)

    verification = ret.ok_value
    return Result.ok(verification)


@Result.shield_exception()
def cancel_subscription(user_id: int) -> Result[CancelResult, FindError]:
    repo = injector.get(SubscriptionInterface)
    ids_ret = repo.get_ids(SubscriptionFilterOption(customer_user_id=user_id), SubscriptionSortOption(is_asc=False))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    subscriptions_ret = repo.bulk_get(ids)
    if subscriptions_ret.is_err:
        return Result.err(subscriptions_ret.err_value)

    subscriptions = subscriptions_ret.ok_value
    not_canceled_at = datetime.min.replace(tzinfo=timezone.utc)
    cancelable_subscriptions = [s for s in subscriptions if s.status in (SubscriptionStatus.ACTIVE, SubscriptionStatus.PAST_DUE) and s.canceled_at == not_canceled_at]
    if len(cancelable_subscriptions) == 0:
        return Result.err(NotFoundError("error.subscriptionNotFound"))

    subscription = cancelable_subscriptions[0]

    customer_repo = injector.get(PaymentCustomerInterface)
    customers_ret = customer_repo.bulk_get([subscription.payment_customer_id])
    if customers_ret.is_err:
        return Result.err(customers_ret.err_value)

    customers = customers_ret.ok_value
    provider = customers[0].provider
    request_ret = atomic_result(lambda: save_cancellation_request_data(provider, subscription.external_id))
    if request_ret.is_err:
        match request_ret.err_value:
            case ValidationError() as error:
                return Result.err(NotFoundError(error.message))
            case ConflictError() | HistoryCorruptedError() | FatalError() as error:
                log.error("Payment cancel request not saved", user_id=user_id, external_id=subscription.external_id, error=str(error))
                return Result.err(FatalError("Payment cancel request not saved"))
            case _:
                assert_never(request_ret.err_value)

    request_id = request_ret.ok_value
    payment_repo = get_payment_repository(provider)
    cancel_ret = payment_repo.cancel_subscription(subscription.external_id, request_id)
    if cancel_ret.is_err:
        return Result.err(cancel_ret.err_value)

    cancellation = cancel_ret.ok_value
    if isinstance(cancellation, CancelFailed):
        if cancellation.error == CancelError.NETWORK_ERROR:
            log.warning("Payment cancel result unknown", user_id=user_id, external_id=subscription.external_id, request_id=request_id)
            return Result.ok(cancellation)

        failure_ret = atomic_result(lambda: save_cancellation_failure_data(provider, subscription.external_id, cancellation.error))
        if failure_ret.is_err:
            log.error("Payment cancel failure not saved", user_id=user_id, external_id=subscription.external_id, error=str(failure_ret.err_value))
            return Result.err(FatalError("Payment cancel failure not saved"))

        return Result.ok(cancellation)

    if isinstance(cancellation, CancelSuccess):
        provider_subscription_ret = payment_repo.get_subscription(subscription.external_id)
        if provider_subscription_ret.is_err:
            return Result.err(provider_subscription_ret.err_value)

        provider_subscription = provider_subscription_ret.ok_value
        save_ret = atomic_result(lambda: save_provider_subscription_data(provider_subscription, datetime.now(timezone.utc)))
        if save_ret.is_err:
            log.error("Payment cancel not saved", user_id=user_id, external_id=subscription.external_id, error=str(save_ret.err_value))
            return Result.err(FatalError("Payment cancel not saved"))

        log.info("Payment cancel succeeded", user_id=user_id, external_id=subscription.external_id)

    return Result.ok(cancellation)


@Result.shield_exception()
def receive_payment_event(event: PaymentEventData) -> Result[bool, FatalError]:
    record_ret = save_payment_event_data(event)
    if record_ret.is_err:
        return Result.err(record_ret.err_value)

    event_id = record_ret.ok_value
    return Result.ok(event_id is not None)


@Result.shield_exception()
def process_payment_events(limit: int) -> Result[int, FatalError]:
    repo = injector.get(PaymentEventInterface)
    filter = PaymentEventFilterOption(is_processed=False, max_attempts=PAYMENT_EVENT_MAX_ATTEMPTS)
    ids_ret = repo.get_ids(filter, PaymentEventSortOption(), limit=limit)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    events_ret = repo.bulk_get(ids)
    if events_ret.is_err:
        return Result.err(events_ret.err_value)

    events = events_ret.ok_value
    processed_count = 0
    for event in events:
        process_ret = atomic_result(lambda: save_processed_payment_event_data(event))
        if process_ret.is_ok:
            processed_count += 1
            continue

        failed_ret = save_failed_payment_event_data(event, process_ret.err_value.message)
        if failed_ret.is_err:
            return Result.err(failed_ret.err_value)

    return Result.ok(processed_count)


@Result.shield_exception()
def requeue_payment_events() -> Result[int, FatalError]:
    repo = injector.get(PaymentEventInterface)
    ids_ret = repo.get_ids(PaymentEventFilterOption(is_processed=False), PaymentEventSortOption(), limit=None)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    events_ret = repo.bulk_get(ids)
    if events_ret.is_err:
        return Result.err(events_ret.err_value)

    events = events_ret.ok_value
    save_ret = repo.bulk_save([replace(event, attempts=0) for event in events])
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    log.info("PaymentEvent requeued", count=len(events))
    return Result.ok(len(events))


@Result.shield_exception()
def replay_payment_events() -> Result[int, CommandError]:
    return atomic_result(lambda: save_payment_projection_data())


@Result.shield_exception()
def export_ledger(start: datetime, end: datetime) -> Result[list[LedgerRowDTO], FatalError]:
    repo = injector.get(LedgerEntryInterface)
    ids_ret = repo.get_ids(LedgerEntryFilterOption(occurred_from=start, occurred_to=end), LedgerEntrySortOption(), limit=None)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    entries_ret = repo.bulk_get(ids)
    if entries_ret.is_err:
        return Result.err(entries_ret.err_value)

    entries = entries_ret.ok_value
    transaction_repo = injector.get(TransactionInterface)
    transactions_ret = transaction_repo.bulk_get(list({e.transaction_id for e in entries}))
    if transactions_ret.is_err:
        return Result.err(transactions_ret.err_value)

    transactions = transactions_ret.ok_value
    customer_repo = injector.get(PaymentCustomerInterface)
    customers_ret = customer_repo.bulk_get(list({t.payment_customer_id for t in transactions}))
    if customers_ret.is_err:
        return Result.err(customers_ret.err_value)

    customers = customers_ret.ok_value
    payout_repo = injector.get(PayoutInterface)
    payouts_ret = payout_repo.bulk_get(list({e.payout_id for e in entries if e.payout_id != 0}))
    if payouts_ret.is_err:
        return Result.err(payouts_ret.err_value)

    payouts = payouts_ret.ok_value
    transaction_map = {t.id: t for t in transactions}
    customer_map = {c.id: c for c in customers}
    payout_map = {p.id: p for p in payouts}
    rows: list[LedgerRowDTO] = []
    for entry in entries:
        transaction = transaction_map[entry.transaction_id]
        payout = payout_map.get(entry.payout_id)
        rows.append(LedgerRowDTO(
            occurred_at=entry.occurred_at,
            provider=customer_map[transaction.payment_customer_id].provider,
            entry_type=entry.entry_type,
            amount=entry.amount,
            tax_amount=entry.tax_amount,
            currency=transaction.currency,
            transaction_external_id=transaction.external_id,
            receipt_number=transaction.receipt_number,
            payout_external_id=payout.external_id if payout is not None else "",
            payout_arrival_at=payout.arrival_at if payout is not None else None,
        ))

    return Result.ok(rows)
