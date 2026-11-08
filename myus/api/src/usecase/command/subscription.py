from datetime import datetime
from api.src.domain.aggregate.subscription.apply import replay
from api.src.domain.aggregate.subscription.decide import accept_provider_state
from api.src.domain.aggregate.subscription.event import SUBSCRIPTION_AGGREGATE_TYPE
from api.src.domain.interface.es.interface import EventStoreInterface
from api.src.domain.interface.payment.event.data import ProviderSubscriptionData
from api.src.injectors.container import injector
from api.src.usecase.command.handler import handle_command
from api.utils.common.result import CommandError, Result


@Result.shield_exception()
def accept_provider_subscription(provider_subscription: ProviderSubscriptionData, occurred_at: datetime) -> Result[None, CommandError]:
    repo = injector.get(EventStoreInterface)
    aggregate_id = f"{provider_subscription.provider.value}:{provider_subscription.external_id}"
    command_ret = handle_command(repo, SUBSCRIPTION_AGGREGATE_TYPE, aggregate_id, replay, lambda state: accept_provider_state(state, provider_subscription, occurred_at), occurred_at)
    if command_ret.is_err:
        return Result.err(command_ret.err_value)

    return Result.ok(None)
