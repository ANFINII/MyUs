from dataclasses import replace
from datetime import datetime, timezone
from typing import assert_never
from myus.domain.payment.customer.interface import PaymentCustomerInterface
from myus.domain.payment.data import Money
from myus.domain.payment.event.data import PaymentEventData
from myus.domain.payment.event.interface import FilterOption as PaymentEventFilterOption, PageOption as PaymentEventPageOption, SortOption as PaymentEventSortOption, PaymentEventInterface
from myus.domain.payment.ledger.interface import FilterOption as LedgerEntryFilterOption, PageOption as LedgerEntryPageOption, SortOption as LedgerEntrySortOption, LedgerEntryInterface
from myus.domain.payment.payout.interface import PayoutInterface
from myus.domain.payment.plan import PLANS, get_plan, plan_price
from myus.domain.payment.product.interface import FilterOption as ProductFilterOption, PageOption as ProductPageOption, ProductInterface, SortOption as ProductSortOption
from myus.domain.payment.provider.data import CancelResult, CancelSuccessData, CancelFailedData, CheckoutData, CheckoutResult, CustomerData, MarketplaceData, PaymentMethodSessionResult, PlanChangeResult, PlanChangeSuccessData, RedirectUrlsData, RevokeResult, RevokeSuccessData, SellerOnboardCreatedData, SellerOnboardData, SellerOnboardResult, SellerStatusFailedData, SellerStatusSuccessData, WebhookVerifyResult
from myus.domain.payment.seller.data import PaymentSellerData
from myus.domain.payment.subscription.data import SubscriptionData
from myus.domain.payment.subscription.interface import FilterOption as SubscriptionFilterOption, PageOption as SubscriptionPageOption, SortOption as SubscriptionSortOption, SubscriptionInterface
from myus.domain.payment.transaction.interface import TransactionInterface
from myus.injectors.container import injector
from myus.utils.common.logger import log
from myus.utils.common.result import AccessError, CommandError, ConflictError, FatalError, FindError, ForbiddenError, HistoryCorruptedError, InputError, NotFoundError, Result, ValidationError
from myus.utils.enum.i18n import Locale
from myus.utils.enum.payment import CancelError, PaymentProvider, PaymentType, SubscriptionStatus
from myus.utils.enum.user import PlanName
from myus.utils.functions.common import create_frontend_url
from myus.utils.functions.map import country_currency, product_media_type
from myus.utils.functions.transaction import atomic_result
from ._convert import get_purchase_ids_data, get_payment_repository, get_payment_seller_data, save_payment_seller_data, get_active_subscription_data, save_payment_event_data, save_provider_subscription_data, save_cancellation_request_data, save_cancellation_failure_data, save_processed_payment_event_data, save_failed_payment_event_data, save_payment_projection_data, save_subscription_projection_data, PAYMENT_EVENT_MAX_ATTEMPTS, PLATFORM_FEE_RATE
from ..dto.ledger import LedgerRowDTO
from ..dto.plan import PlanPriceDTO
from ..dto.seller import SellerDTO
from ..media._convert import get_media_repository
from ..user.core import get_user_data


CHECKOUT_PROVIDER = PaymentProvider.STRIPE


@Result.shield_exception()
def create_checkout(user_id: int, plan_name: str, locale: Locale) -> Result[CheckoutResult, InputError]:
    user_ret = get_user_data(user_id=user_id)
    if user_ret.is_err:
        return Result.err(user_ret.err_value)

    user = user_ret.ok_value
    if user is None:
        return Result.err(NotFoundError("error.userNotFound"))

    plan = get_plan(plan_name)
    if plan is None:
        log.warning("unknown plan", plan=plan_name)
        return Result.err(NotFoundError("error.planNotFound"))

    subscription_repo = injector.get(SubscriptionInterface)
    subscription_ids_ret = subscription_repo.get_ids(SubscriptionFilterOption(customer_user_id=user_id), SubscriptionSortOption(), SubscriptionPageOption())
    if subscription_ids_ret.is_err:
        return Result.err(subscription_ids_ret.err_value)

    subscription_ids = subscription_ids_ret.ok_value
    subscriptions_ret = subscription_repo.bulk_get(subscription_ids)
    if subscriptions_ret.is_err:
        return Result.err(subscriptions_ret.err_value)

    subscriptions = subscriptions_ret.ok_value
    if any(s.status in (SubscriptionStatus.ACTIVE, SubscriptionStatus.PAST_DUE) for s in subscriptions):
        log.warning("already subscribed", user_id=user_id, plan=plan_name)
        return Result.err(ValidationError("error.alreadySubscribed"))

    currency = country_currency(user.profile.country)
    frontend_url = create_frontend_url(locale)
    data = CheckoutData(
        product_code=plan.name,
        description=plan.description,
        price=plan_price(plan, currency),
        payment_type=PaymentType.SUBSCRIPTION,
        customer=CustomerData(user_ulid=user.user.ulid, email=user.user.email),
        redirect=RedirectUrlsData(
            success_url=f"{frontend_url}/setting/payment/success",
            cancel_url=f"{frontend_url}/setting/payment/cancel",
        ),
        marketplace=MarketplaceData(seller_id="", application_fee=Money(amount=0, currency=currency)),
        locale=locale,
    )

    repo = get_payment_repository(CHECKOUT_PROVIDER)
    checkout_ret = repo.create_checkout(data)
    if checkout_ret.is_err:
        return Result.err(checkout_ret.err_value)

    checkout = checkout_ret.ok_value
    return Result.ok(checkout)


@Result.shield_exception()
def create_product_checkout(user_id: int, product_ulid: str, locale: Locale) -> Result[CheckoutResult, InputError]:
    user_ret = get_user_data(user_id=user_id)
    if user_ret.is_err:
        return Result.err(user_ret.err_value)

    user = user_ret.ok_value
    if user is None:
        return Result.err(NotFoundError("error.userNotFound"))

    repo = injector.get(ProductInterface)
    ids_ret = repo.get_ids(ProductFilterOption(ulid=product_ulid), ProductSortOption(), ProductPageOption(limit=1))
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        log.warning("not paid content", product_ulid=product_ulid)
        return Result.err(ValidationError("error.notPaidContent"))

    products_ret = repo.bulk_get(ids)
    if products_ret.is_err:
        return Result.err(products_ret.err_value)

    products = products_ret.ok_value
    product = products[0]
    media_type = product_media_type(product.product_type)
    media_repo = get_media_repository(media_type)
    objs_ret = media_repo.bulk_get([product.object_id])
    if objs_ret.is_err:
        return Result.err(objs_ret.err_value)

    objs = objs_ret.ok_value
    if len(objs) == 0 or not objs[0].publish:
        log.info("not found", product_ulid=product_ulid)
        return Result.err(NotFoundError("error.mediaNotFound"))

    obj = objs[0]
    if product.seller_id == user_id:
        log.warning("own content", product_ulid=product_ulid, user_id=user_id)
        return Result.err(ValidationError("error.purchaseOwnContent"))

    purchase_ids_ret = get_purchase_ids_data([product.id], user_id)
    if purchase_ids_ret.is_err:
        return Result.err(purchase_ids_ret.err_value)

    purchase_ids = purchase_ids_ret.ok_value
    if len(purchase_ids) > 0:
        log.warning("already purchased", product_ulid=product_ulid, user_id=user_id)
        return Result.err(ValidationError("error.alreadyPurchased"))

    seller_ret = get_payment_seller_data(product.seller_id)
    if seller_ret.is_err:
        return Result.err(seller_ret.err_value)

    seller = seller_ret.ok_value
    if seller is None or not seller.is_enabled:
        log.warning("seller not enabled", product_ulid=product_ulid, seller_id=product.seller_id)
        return Result.err(ValidationError("error.sellerNotEnabled"))

    media_url = f"{create_frontend_url(locale)}/media/{media_type.value.lower()}/{obj.ulid}"
    data = CheckoutData(
        product_code=product.ulid,
        description=obj.title,
        price=product.price,
        payment_type=PaymentType.ONE_TIME,
        customer=CustomerData(user_ulid=user.user.ulid, email=user.user.email),
        redirect=RedirectUrlsData(success_url=media_url, cancel_url=media_url),
        marketplace=MarketplaceData(seller_id=seller.external_id, application_fee=Money(amount=product.price.amount * PLATFORM_FEE_RATE // 100, currency=product.price.currency)),
        locale=locale,
    )

    payment_repo = get_payment_repository(seller.provider)
    checkout_ret = payment_repo.create_checkout(data)
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
def get_subscription(user_id: int) -> Result[SubscriptionData | None, FatalError]:
    repo = injector.get(SubscriptionInterface)
    ids_ret = repo.get_ids(SubscriptionFilterOption(customer_user_id=user_id), SubscriptionSortOption(is_asc=False), SubscriptionPageOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    subscriptions_ret = repo.bulk_get(ids)
    if subscriptions_ret.is_err:
        return Result.err(subscriptions_ret.err_value)

    subscriptions = subscriptions_ret.ok_value
    current_subscriptions = [s for s in subscriptions if s.status in (SubscriptionStatus.ACTIVE, SubscriptionStatus.PAST_DUE)]
    if len(current_subscriptions) == 0:
        return Result.ok(None)

    return Result.ok(current_subscriptions[0])


@Result.shield_exception()
def get_plan_prices(user_id: int) -> Result[list[PlanPriceDTO], FindError]:
    subscription_ret = get_subscription(user_id)
    if subscription_ret.is_err:
        return Result.err(subscription_ret.err_value)

    subscription = subscription_ret.ok_value
    if subscription is not None:
        currency = subscription.price.currency
    else:
        user_ret = get_user_data(user_id=user_id)
        if user_ret.is_err:
            return Result.err(user_ret.err_value)

        user = user_ret.ok_value
        if user is None:
            return Result.err(NotFoundError("error.userNotFound"))

        currency = country_currency(user.profile.country)

    return Result.ok([PlanPriceDTO(name=p.name, price=plan_price(p, currency)) for p in PLANS])


@Result.shield_exception()
def cancel_subscription(user_id: int) -> Result[CancelResult, FindError]:
    subscription_ret = get_active_subscription_data(user_id)
    if subscription_ret.is_err:
        return Result.err(subscription_ret.err_value)

    subscription = subscription_ret.ok_value
    if subscription is None:
        return Result.err(NotFoundError("error.subscriptionNotFound"))

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
                log.error("cancel request not saved", user_id=user_id, external_id=subscription.external_id, error=str(error))
                return Result.err(FatalError("Payment cancel request not saved"))
            case _:
                assert_never(request_ret.err_value)

    request_id = request_ret.ok_value
    payment_repo = get_payment_repository(provider)
    cancel_ret = payment_repo.cancel_subscription(subscription.external_id, request_id)
    if cancel_ret.is_err:
        return Result.err(cancel_ret.err_value)

    cancellation = cancel_ret.ok_value
    if isinstance(cancellation, CancelFailedData):
        if cancellation.error == CancelError.NETWORK_ERROR:
            log.warning("cancel result unknown", user_id=user_id, external_id=subscription.external_id, request_id=request_id)
            return Result.ok(cancellation)

        failure_ret = atomic_result(lambda: save_cancellation_failure_data(provider, subscription.external_id, cancellation.error))
        if failure_ret.is_err:
            log.error("cancel failure not saved", user_id=user_id, external_id=subscription.external_id, error=str(failure_ret.err_value))
            return Result.err(FatalError("Payment cancel failure not saved"))

        return Result.ok(cancellation)

    if isinstance(cancellation, CancelSuccessData):
        provider_subscription_ret = payment_repo.get_subscription(subscription.external_id)
        if provider_subscription_ret.is_err:
            return Result.err(provider_subscription_ret.err_value)

        provider_subscription = provider_subscription_ret.ok_value
        save_ret = atomic_result(lambda: save_provider_subscription_data(provider_subscription, datetime.now(timezone.utc)))
        if save_ret.is_err:
            log.error("cancel not saved", user_id=user_id, external_id=subscription.external_id, error=str(save_ret.err_value))
            return Result.err(FatalError("Payment cancel not saved"))

        log.info("cancel succeeded", user_id=user_id, external_id=subscription.external_id)

    return Result.ok(cancellation)


@Result.shield_exception()
def revoke_cancellation(user_id: int) -> Result[RevokeResult, InputError]:
    subscription_ret = get_subscription(user_id)
    if subscription_ret.is_err:
        return Result.err(subscription_ret.err_value)

    subscription = subscription_ret.ok_value
    if subscription is None:
        return Result.err(NotFoundError("error.subscriptionNotFound"))

    if subscription.canceled_at == datetime.min.replace(tzinfo=timezone.utc):
        return Result.err(ValidationError("error.cancellationNotScheduled"))

    customer_repo = injector.get(PaymentCustomerInterface)
    customers_ret = customer_repo.bulk_get([subscription.payment_customer_id])
    if customers_ret.is_err:
        return Result.err(customers_ret.err_value)

    customers = customers_ret.ok_value
    repo = get_payment_repository(customers[0].provider)
    revoke_ret = repo.revoke_cancellation(subscription.external_id)
    if revoke_ret.is_err:
        return Result.err(revoke_ret.err_value)

    revoke = revoke_ret.ok_value
    if isinstance(revoke, RevokeSuccessData):
        save_ret = atomic_result(lambda: save_provider_subscription_data(revoke.subscription, datetime.now(timezone.utc)))
        if save_ret.is_err:
            log.error("cancel revoke not saved", user_id=user_id, external_id=subscription.external_id, error=str(save_ret.err_value))
            return Result.err(FatalError("Payment cancel revoke not saved"))

        log.info("cancel revoked", user_id=user_id, external_id=subscription.external_id)

    return Result.ok(revoke)


@Result.shield_exception()
def change_plan(user_id: int, plan_name: str) -> Result[PlanChangeResult, InputError]:
    plan = get_plan(plan_name)
    if plan is None:
        log.warning("unknown plan", plan=plan_name)
        return Result.err(NotFoundError("error.planNotFound"))

    if plan.name == PlanName.FREE:
        return Result.err(ValidationError("error.planChangeToFree"))

    subscription_ret = get_active_subscription_data(user_id)
    if subscription_ret.is_err:
        return Result.err(subscription_ret.err_value)

    subscription = subscription_ret.ok_value
    if subscription is None:
        return Result.err(NotFoundError("error.subscriptionNotFound"))

    if subscription.product_code == plan.name:
        return Result.err(ValidationError("error.planChangeSame"))

    customer_repo = injector.get(PaymentCustomerInterface)
    customers_ret = customer_repo.bulk_get([subscription.payment_customer_id])
    if customers_ret.is_err:
        return Result.err(customers_ret.err_value)

    customers = customers_ret.ok_value
    repo = get_payment_repository(customers[0].provider)
    change_ret = repo.change_plan(subscription.external_id, plan.name)
    if change_ret.is_err:
        return Result.err(change_ret.err_value)

    change = change_ret.ok_value
    if isinstance(change, PlanChangeSuccessData):
        save_ret = atomic_result(lambda: save_provider_subscription_data(change.subscription, datetime.now(timezone.utc)))
        if save_ret.is_err:
            log.error("plan change not saved", user_id=user_id, external_id=subscription.external_id, error=str(save_ret.err_value))
            return Result.err(FatalError("Payment plan change not saved"))

        log.info("plan changed", user_id=user_id, external_id=subscription.external_id, plan=plan_name)

    return Result.ok(change)


@Result.shield_exception()
def create_payment_method_session(user_id: int, locale: Locale) -> Result[PaymentMethodSessionResult, FindError]:
    subscription_ret = get_subscription(user_id)
    if subscription_ret.is_err:
        return Result.err(subscription_ret.err_value)

    subscription = subscription_ret.ok_value
    if subscription is None:
        return Result.err(NotFoundError("error.subscriptionNotFound"))

    customer_repo = injector.get(PaymentCustomerInterface)
    customers_ret = customer_repo.bulk_get([subscription.payment_customer_id])
    if customers_ret.is_err:
        return Result.err(customers_ret.err_value)

    customers = customers_ret.ok_value
    customer = customers[0]
    return_url = f"{create_frontend_url(locale)}/setting/payment"
    repo = get_payment_repository(customer.provider)
    session_ret = repo.create_payment_method_session(customer.external_id, return_url, locale)
    if session_ret.is_err:
        return Result.err(session_ret.err_value)

    session = session_ret.ok_value
    return Result.ok(session)


@Result.shield_exception()
def get_seller(user_id: int) -> Result[SellerDTO, FindError]:
    user_ret = get_user_data(user_id=user_id)
    if user_ret.is_err:
        return Result.err(user_ret.err_value)

    user = user_ret.ok_value
    if user is None:
        return Result.err(NotFoundError("error.userNotFound"))

    plan = get_plan(user.user_plan.plan)
    is_available = plan is not None and plan.is_paid_content
    currency = country_currency(user.profile.country)

    seller_ret = get_payment_seller_data(user_id)
    if seller_ret.is_err:
        return Result.err(seller_ret.err_value)

    seller = seller_ret.ok_value
    if seller is None:
        return Result.ok(SellerDTO(is_available=is_available, is_registered=False, is_enabled=False, currency=currency))

    if seller.is_enabled:
        return Result.ok(SellerDTO(is_available=is_available, is_registered=True, is_enabled=True, currency=currency))

    repo = get_payment_repository(seller.provider)
    status_ret = repo.get_seller(seller.external_id)
    if status_ret.is_err:
        return Result.err(status_ret.err_value)

    status = status_ret.ok_value
    match status:
        case SellerStatusSuccessData(is_enabled=is_enabled):
            if is_enabled != seller.is_enabled:
                save_ret = save_payment_seller_data(replace(seller, is_enabled=is_enabled))
                if save_ret.is_err:
                    return Result.err(save_ret.err_value)
            return Result.ok(SellerDTO(is_available=is_available, is_registered=True, is_enabled=is_enabled, currency=currency))
        case SellerStatusFailedData(error=error, message=message):
            log.warning("seller status failed", user_id=user_id, error=error.value, message=message)
            return Result.ok(SellerDTO(is_available=is_available, is_registered=True, is_enabled=seller.is_enabled, currency=currency))
        case _:
            assert_never(status)


@Result.shield_exception()
def onboard_seller(user_id: int, locale: Locale) -> Result[SellerOnboardResult, AccessError]:
    user_ret = get_user_data(user_id=user_id)
    if user_ret.is_err:
        return Result.err(user_ret.err_value)

    user = user_ret.ok_value
    if user is None:
        return Result.err(NotFoundError("error.userNotFound"))

    plan = get_plan(user.user_plan.plan)
    if plan is None or not plan.is_paid_content:
        log.info("plan required", user_id=user_id)
        return Result.err(ForbiddenError("error.paidContentPlanRequired"))

    seller_ret = get_payment_seller_data(user_id)
    if seller_ret.is_err:
        return Result.err(seller_ret.err_value)

    seller = seller_ret.ok_value
    provider = seller.provider if seller is not None else CHECKOUT_PROVIDER
    return_url = f"{create_frontend_url(locale)}/setting/payment"
    data = SellerOnboardData(
        external_id=seller.external_id if seller is not None else "",
        user_ulid=user.user.ulid,
        email=user.user.email,
        country=user.profile.country,
        return_url=return_url,
        refresh_url=return_url,
    )

    repo = get_payment_repository(provider)
    onboard_ret = repo.onboard_seller(data)
    if onboard_ret.is_err:
        return Result.err(onboard_ret.err_value)

    onboard = onboard_ret.ok_value
    if isinstance(onboard, SellerOnboardCreatedData) and seller is None:
        save_ret = save_payment_seller_data(PaymentSellerData(id=0, user_id=user_id, provider=provider, external_id=onboard.external_id, is_enabled=False))
        if save_ret.is_err:
            return Result.err(save_ret.err_value)

    return Result.ok(onboard)


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
    ids_ret = repo.get_ids(filter, PaymentEventSortOption(), PaymentEventPageOption(limit=limit))
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
    ids_ret = repo.get_ids(PaymentEventFilterOption(is_processed=False), PaymentEventSortOption(), PaymentEventPageOption())
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

    log.info("requeued", count=len(events))
    return Result.ok(len(events))


@Result.shield_exception()
def replay_payment_events() -> Result[int, CommandError]:
    return atomic_result(lambda: save_payment_projection_data())


@Result.shield_exception()
def reproject_subscriptions() -> Result[int, CommandError]:
    return atomic_result(lambda: save_subscription_projection_data())


@Result.shield_exception()
def export_ledger(start: datetime, end: datetime) -> Result[list[LedgerRowDTO], FatalError]:
    repo = injector.get(LedgerEntryInterface)
    ids_ret = repo.get_ids(LedgerEntryFilterOption(occurred_from=start, occurred_to=end), LedgerEntrySortOption(), LedgerEntryPageOption())
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
