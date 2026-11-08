from django.core.management.base import BaseCommand
from api.modules.logger import log
from api.src.usecase.payment.core import requeue_payment_events


class Command(BaseCommand):
    help = "反映を諦めた PaymentEvent（失敗が上限に達したもの）の失敗回数を 0 に戻し、worker がもう一度反映するようにする"

    def handle(self, *args, **options):
        ret = requeue_payment_events()
        if ret.is_err:
            log.error("PaymentEvent requeue command failed", error=ret.err_value.message)
            self.stderr.write(self.style.ERROR("戻せませんでした"))
            return

        count = ret.ok_value
        self.stdout.write(self.style.SUCCESS(f"Requeued {count} payment events"))
