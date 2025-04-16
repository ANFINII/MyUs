import coloredlogs
from logging import getLogger, INFO, Formatter, StreamHandler


class Log:
    formatter = Formatter("%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    logger = getLogger(__name__)
    logger.setLevel(INFO)
    stream_handler = StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    coloredlogs.install(
        level="INFO",
        logger=logger,
        fmt="%(asctime)s - %(levelname)s %(message)s",
        level_styles={"info": {"color": "black"}, "error": {"color": "red"}},
        field_styles={"asctime": {"color": "green"}, "levelname": {"color": "blue"}, "message": {"color": "black"}}
    )

    @staticmethod
    def info(cls: str | None, func: str | None, msg: str | None):
        logs = ""
        logs += f"| class: {cls} " if cls else ""
        logs += f"| def: {func} " if func else ""
        logs += f"| message: {msg} " if msg else ""
        Log.logger.info(logs + "\n")

    @staticmethod
    def error(cls: str | None, func: str | None, msg: str | None):
        logs = ""
        logs += f"| class: {cls} " if cls else ""
        logs += f"| def: {func} " if func else ""
        logs += f"| message: {msg} " if msg else ""
        Log.logger.error(logs + "\n")
