from django.core.management.base import BaseCommand
from api.modules.logger import log
from api.src.domain.interface.webhook.outbox.interface import FilterOption, SortOption, WebhookOutboxInterface
from api.src.injectors.container import injector
from api.utils.enum.payment import WebhookDeliveryStatus


class Command(BaseCommand):
    help = "PENDING の WebhookOutbox を配信する（送信先が未定のため、今は件数を出すだけで状態は変えない）"

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=20, help="一度に処理する最大件数")

    def handle(self, *args, **options):
        limit = options["limit"]

        repo = injector.get(WebhookOutboxInterface)
        ids_ret = repo.get_ids(
            FilterOption(status=WebhookDeliveryStatus.PENDING.value),
            SortOption(),
            limit=limit,
        )
        if ids_ret.is_err:
            log.error("WebhookOutbox dispatch get_ids failed", error=ids_ret.err_value.message)
            return

        ids = ids_ret.ok_value
        if len(ids) == 0:
            log.info("WebhookOutbox dispatch no pending entries")
            self.stdout.write(self.style.SUCCESS("No pending webhook outbox entries"))
            return

        log.warning("WebhookOutbox delivery is not implemented", count=len(ids))
        self.stdout.write(self.style.WARNING(f"Delivery is not implemented: {len(ids)} webhook outbox entries remain pending"))
