import time
from django.core.management.base import BaseCommand
from myus.usecase.encode.core import encode_audios, encode_videos
from myus.utils.common.logger import log


class Command(BaseCommand):
    help = "まだ変換していない動画を古い順に HLS に、オーディオを MP3 に変換する。--once が無ければ繰り返す（worker）"

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=1, help="一度に処理する最大件数")
        parser.add_argument("--interval", type=int, default=5, help="繰り返すときの間隔（秒）")
        parser.add_argument("--once", action="store_true", help="1回だけ処理して終わる")

    def handle(self, *args, **options):
        while True:
            video_ret = encode_videos(options["limit"])
            if video_ret.is_err:
                log.error("command failed", error=video_ret.err_value.message)
            else:
                video_count = video_ret.ok_value
                if video_count > 0:
                    log.info("encoded", media_type="video", count=video_count)

            audio_ret = encode_audios(options["limit"])
            if audio_ret.is_err:
                log.error("command failed", error=audio_ret.err_value.message)
            else:
                audio_count = audio_ret.ok_value
                if audio_count > 0:
                    log.info("encoded", media_type="audio", count=audio_count)

            if options["once"]:
                return

            time.sleep(options["interval"])
