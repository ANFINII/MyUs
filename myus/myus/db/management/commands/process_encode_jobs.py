import time
from django.core.management.base import BaseCommand
from myus.usecase.encode_job.core import process_encode_jobs
from myus.utils.common.logger import log


class Command(BaseCommand):
    help = "まだ変換していない動画を古い順に HLS に変換する。--once が無ければ繰り返す（worker）"

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=1, help="一度に処理する最大件数")
        parser.add_argument("--interval", type=int, default=5, help="繰り返すときの間隔（秒）")
        parser.add_argument("--once", action="store_true", help="1回だけ処理して終わる")

    def handle(self, *args, **options):
        while True:
            ret = process_encode_jobs(options["limit"])
            if ret.is_err:
                log.error("command failed", error=ret.err_value.message)
            else:
                count = ret.ok_value
                if count > 0:
                    log.info("processed", count=count)

            if options["once"]:
                return

            time.sleep(options["interval"])
