from django.core.management.base import BaseCommand
from myus.usecase.encode.core import measure_music_gains
from myus.utils.common.logger import log


class Command(BaseCommand):
    help = "すべての曲の大きさを測り直し、再生時に下げる音量を保存する"

    def handle(self, *args, **options):
        ret = measure_music_gains()
        if ret.is_err:
            log.error("command failed", error=ret.err_value.message)
            return

        count = ret.ok_value
        log.info("measured", count=count)
