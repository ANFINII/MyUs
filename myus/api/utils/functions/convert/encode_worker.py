import os
from concurrent.futures import ThreadPoolExecutor
from django.conf import settings
from api.modules.logger import log


class EncodeWorker:
    """バックグラウンドでエンコードを実行するワーカー"""

    _executor: ThreadPoolExecutor | None = None

    @classmethod
    def get_executor(cls) -> ThreadPoolExecutor:
        if cls._executor is None:
            workers = max(os.cpu_count() or 1, 2)
            cls._executor = ThreadPoolExecutor(max_workers=workers, thread_name_prefix="encode")
            log.info("EncodeWorker 起動", workers=workers)
        return cls._executor

    @classmethod
    def submit_video(cls, video_id: int, video_path: str) -> None:
        """動画エンコードをバックグラウンドで実行"""
        cls.get_executor().submit(cls._encode_and_update, video_id, video_path)
        log.info("エンコードタスク投入", video_id=video_id, video_path=video_path)

    @classmethod
    def _encode_and_update(cls, video_id: int, video_path: str) -> None:
        """エンコード実行後にDBを更新"""
        import django
        django.setup()

        from api.db.models.media import Video
        from api.utils.functions.convert.video_encoding import encode_video

        absolute_path = os.path.join(settings.MEDIA_ROOT, video_path)
        output_dir = os.path.dirname(absolute_path)
        video_dir = os.path.dirname(video_path)
        video_name = os.path.splitext(os.path.basename(video_path))[0]

        try:
            encode_video(convert_path=absolute_path, output_dir=output_dir)
            master_path = os.path.join(video_dir, f"{video_name}_master.m3u8")
            convert_path = os.path.join(video_dir, f"{video_name}_convert.mp4")

            Video.objects.filter(id=video_id).update(video=master_path, convert=convert_path, publish=True)
            log.info("エンコード完了・DB更新", video_id=video_id, video=master_path, convert=convert_path)
        except Exception as e:
            log.error("エンコード失敗", exc=e, video_id=video_id, video_path=video_path)
