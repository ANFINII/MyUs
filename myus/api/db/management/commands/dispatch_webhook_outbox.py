from dataclasses import replace
from datetime import datetime, timezone
from django.core.management.base import BaseCommand
from api.modules.logger import log
from api.src.domain.interface.webhook.outbox.data import WebhookOutboxData
from api.src.domain.interface.webhook.outbox.interface import FilterOption, SortOption, WebhookOutboxInterface
from api.src.injectors.container import injector
from api.utils.enum.payment import WebhookDeliveryStatus


class Command(BaseCommand):
    help = "PENDING の WebhookOutbox を配信して DELIVERED に更新する"

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=20, help="一度に処理する最大件数")

    def handle(self, *args, **options):
        limit = options["limit"]

        repo = injector.get(WebhookOutboxInterface)
        ids = repo.get_ids(
            FilterOption(status=WebhookDeliveryStatus.PENDING.value),
            SortOption(),
            limit=limit,
        )
        if len(ids) == 0:
            log.info("WebhookOutbox dispatch no pending entries")
            self.stdout.write(self.style.SUCCESS("No pending webhook outbox entries"))
            return

        entries = repo.bulk_get(ids)
        delivered: list[WebhookOutboxData] = []
        for entry in entries:
            # 配信スタブ: 外部送信先が未定のためログ出力で代替する
            log.info("WebhookOutbox delivered (stub)", event_type=entry.event_type.value, external_id=entry.external_id, payload=entry.payload)
            delivered.append(replace(entry, status=WebhookDeliveryStatus.DELIVERED, delivered_at=datetime.now(timezone.utc)))

        repo.bulk_save(delivered)
        log.info("WebhookOutbox dispatch completed", count=len(delivered))
        self.stdout.write(self.style.SUCCESS(f"Dispatched {len(delivered)} webhook outbox entries"))
