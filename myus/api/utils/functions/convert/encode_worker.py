import os
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from api.modules.logger import log


class EncodeWorker:
    """バックグラウンドでタスクを実行するワーカー"""

    _executor: ThreadPoolExecutor | None = None

    @classmethod
    def get_executor(cls) -> ThreadPoolExecutor:
        if cls._executor is None:
            workers = max(os.cpu_count() or 1, 2)
            cls._executor = ThreadPoolExecutor(max_workers=workers, thread_name_prefix="encode")
            log.info("EncodeWorker 起動", workers=workers)
        return cls._executor

    @classmethod
    def submit(cls, task: Callable[[], None]) -> None:
        """タスクをバックグラウンドで実行"""
        cls.get_executor().submit(cls._run, task)

    @classmethod
    def _run(cls, task: Callable[[], None]) -> None:
        try:
            task()
        except Exception as e:
            log.error("バックグラウンドタスク失敗", exc=e)
