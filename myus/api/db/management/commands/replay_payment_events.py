from django.core.management.base import BaseCommand
from api.modules.logger import log
from api.src.usecase.payment.core import replay_payment_events


class Command(BaseCommand):
    help = "決済の取引・明細・入金・サブスクリプションを消し、PaymentEvent を古い順に流し直して作り直す"

    def add_arguments(self, parser):
        parser.add_argument("--confirm", action="store_true", help="取引・明細・入金・サブスクリプションを消して作り直すことに同意する")

    def handle(self, *args, **options):
        if not options["confirm"]:
            self.stdout.write(self.style.WARNING("取引・明細・入金・サブスクリプションを消して作り直します。実行するには --confirm を付けてください"))
            return

        ret = replay_payment_events()
        if ret.is_err:
            log.error("PaymentEvent replay command failed", error=ret.err_value.message)
            self.stderr.write(self.style.ERROR("作り直しに失敗しました。何も変わっていません"))
            return

        count = ret.ok_value
        self.stdout.write(self.style.SUCCESS(f"Replayed {count} payment events"))
