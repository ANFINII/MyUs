from typing import assert_never
from django.core.management.base import BaseCommand
from myus.usecase.payment.core import reproject_subscriptions
from myus.utils.common.logger import log
from myus.utils.enum.es import ProjectorName


class Command(BaseCommand):
    help = "Projector の投影と進捗を消し、es_event から作り直す。流す前に worker を止める"

    def add_arguments(self, parser):
        parser.add_argument("--projector", required=True, choices=[p.value for p in ProjectorName], help="作り直す Projector")
        parser.add_argument("--confirm", action="store_true", help="投影と進捗を消して作り直すことに同意する")

    def handle(self, *args, **options):
        projector = ProjectorName(options["projector"])
        if not options["confirm"]:
            self.stdout.write(self.style.WARNING(f"{projector.value} の投影と進捗を消して作り直します。実行するには --confirm を付けてください"))
            return

        match projector:
            case ProjectorName.SUBSCRIPTION:
                ret = reproject_subscriptions()
            case _:
                assert_never(projector)

        if ret.is_err:
            log.error("command failed", error=ret.err_value.message)
            self.stderr.write(self.style.ERROR("作り直しに失敗しました。何も変わっていません"))
            return

        count = ret.ok_value
        self.stdout.write(self.style.SUCCESS(f"Reprojected {count} aggregates"))
