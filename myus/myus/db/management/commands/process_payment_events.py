import time
from django.core.management.base import BaseCommand
from myus.usecase.payment.core import process_payment_events
from myus.utils.common.logger import log


class Command(BaseCommand):
    help = "webhook で受けた PaymentEvent のうち、まだ反映していないものを古い順に反映する。--once が無ければ繰り返す（worker）"

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=100, help="一度に処理する最大件数")
        parser.add_argument("--interval", type=int, default=10, help="繰り返すときの間隔（秒）")
        parser.add_argument("--once", action="store_true", help="1回だけ処理して終わる")

    def handle(self, *args, **options):
        while True:
            ret = process_payment_events(options["limit"])
            if ret.is_err:
                log.error("PaymentEvent process command failed", error=ret.err_value.message)
            else:
                count = ret.ok_value
                if count > 0:
                    log.info("PaymentEvent processed", count=count)

            if options["once"]:
                return

            time.sleep(options["interval"])
