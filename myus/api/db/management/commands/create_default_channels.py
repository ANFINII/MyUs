from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from api.db.models.channel import Channel
from api.db.models.user import User
from api.modules.logger import log


class Command(BaseCommand):
    help = "デフォルトのチャンネルがないユーザーに、デフォルトのチャンネルを設定する"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--dry-run", action="store_true", help="データを変更せず、対象のユーザー数だけを表示する")

    def handle(self, *args: Any, **options: Any) -> None:
        dry_run = bool(options["dry_run"])
        created_count = 0
        updated_count = 0

        with transaction.atomic():
            for user in User.objects.all():
                channels = Channel.objects.filter(owner=user).order_by("created", "id")
                if not channels.exists():
                    created_count += 1
                    if not dry_run:
                        Channel.objects.create(owner=user, name=user.nickname, is_default=True)
                    continue

                if channels.filter(is_default=True).exists():
                    continue

                first = channels.first()
                if first is None:
                    continue

                updated_count += 1
                if not dry_run:
                    first.is_default = True
                    first.save(update_fields=["is_default"])

        log.info("create_default_channels", dry_run=dry_run, created_count=created_count, updated_count=updated_count)
        self.stdout.write(self.style.SUCCESS(f"作成: {created_count} 件 / デフォルトに設定: {updated_count} 件（dry_run={dry_run}）"))
