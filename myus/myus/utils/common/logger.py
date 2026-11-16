import coloredlogs
import inspect
import json
import re
import traceback
from datetime import UTC, datetime
from enum import Enum
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING, FileHandler, Formatter, Logger, LogRecord, StreamHandler, getLogger
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Any, ClassVar, Literal, Self, assert_never
from config.env import env


type CallerInfo = tuple[str, str, int]
type LogLevel = int
type LevelName = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Color(str, Enum):
    """ANSIエスケープコードによる色定義"""
    # リセット
    RESET = "\033[0m"

    # スタイル
    BOLD = "\033[1m"

    # 基本色（前景色）
    BLACK   = "\033[30m"
    RED     = "\033[31m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    BLUE    = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN    = "\033[36m"
    WHITE   = "\033[37m"

    # 明るい色（前景色）
    BRIGHT_BLACK   = "\033[90m"
    BRIGHT_RED     = "\033[91m"
    BRIGHT_GREEN   = "\033[92m"
    BRIGHT_YELLOW  = "\033[93m"
    BRIGHT_BLUE    = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN    = "\033[96m"
    BRIGHT_WHITE   = "\033[97m"

    # 背景色
    BG_BLACK   = "\033[40m"
    BG_RED     = "\033[41m"
    BG_GREEN   = "\033[42m"
    BG_YELLOW  = "\033[43m"
    BG_BLUE    = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN    = "\033[46m"
    BG_WHITE   = "\033[47m"

    def __str__(self) -> str:
        return self


class ColorFormat(coloredlogs.ColoredFormatter):
    """coloredlogs を継承してログレベルの色をカスタマイズ"""

    LEVEL_COLORS = {
        "DEBUG"   : Color.BLACK,
        "INFO"    : Color.GREEN,
        "WARNING" : Color.YELLOW,
        "ERROR"   : Color.RED,
        "CRITICAL": Color.RED + Color.BOLD
    }

    def format(self, record: LogRecord) -> str:
        levelname = record.levelname
        if levelname in self.LEVEL_COLORS:
            record.levelname = f"{self.LEVEL_COLORS[levelname]}{levelname}{Color.RESET}"

        result: str = super().format(record)
        record.levelname = levelname
        return result


class PlainFormatter(Formatter):
    """ファイル用：ANSIの色コードを取り除く"""

    ANSI_PATTERN: ClassVar[re.Pattern[str]] = re.compile(r"\x1b\[[0-9;]*m")

    def format(self, record: LogRecord) -> str:
        return self.ANSI_PATTERN.sub("", super().format(record))


class Log:
    """ログクラス - 自動呼び出し元検出とスタックトレース対応"""

    # ログ設定
    LOG_FORMAT: ClassVar[str] = "[%(asctime)s] - %(name)s - %(levelname)s - %(message)s"
    DATE_FORMAT: ClassVar[str] = "%Y-%m-%d %H:%M:%S"

    # カラー設定
    LEVEL_STYLES: ClassVar[dict[str, dict[str, Any]]] = {
        "debug"   : {"color": "blue"},
        "info"    : {"color": "green"},
        "warning" : {"color": "yellow", "bold": False},
        "error"   : {"color": "red", "bold": False},
        "critical": {"color": "red", "bold": True}
    }

    FIELD_STYLES: ClassVar[dict[str, dict[str, Any]]] = {
        "asctime"  : {"color": "blue"},
        "name"     : {"color": "yellow"},
        "levelname": {"color": "white", "bold": True},
        "message"  : {"color": "white"}
    }

    # レベルマッピング
    LEVEL_MAP: ClassVar[dict[str, LogLevel]] = {
        "DEBUG": DEBUG,
        "INFO": INFO,
        "WARNING": WARNING,
        "ERROR": ERROR,
        "CRITICAL": CRITICAL
    }

    # 本番は1行の JSON、開発は色付きの文字列で出す
    IS_JSON: ClassVar[bool] = not env.debug
    JSON_RESERVED_KEYS: ClassVar[frozenset[str]] = frozenset({"timestamp", "level", "message", "file", "line", "func", "exception", "traceback"})

    # シングルトンインスタンス
    _instance: ClassVar[Self | None] = None
    _logger: Logger | None = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self) -> None:
        """ロガーの初期化"""
        self._logger = getLogger("MyUs")
        self._logger.setLevel(DEBUG)

        # 既存のハンドラーをクリア
        self._logger.handlers.clear()

        # ファイルハンドラー（エラー以上）
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        error_file_handler = TimedRotatingFileHandler(
            log_dir / "error.log",
            when="midnight",
            backupCount=30,
            encoding="utf-8"
        )
        error_file_handler.setLevel(ERROR)
        error_file_handler.setFormatter(Formatter("%(message)s") if self.IS_JSON else PlainFormatter(self.LOG_FORMAT, self.DATE_FORMAT))
        self._logger.addHandler(error_file_handler)

        if self.IS_JSON:
            stream_handler = StreamHandler()
            stream_handler.setLevel(INFO)
            stream_handler.setFormatter(Formatter("%(message)s"))
            self._logger.addHandler(stream_handler)
            return

        # coloredlogsを使用して色を設定
        coloredlogs.install(
            level=INFO,
            logger=self._logger,
            fmt=self.LOG_FORMAT,
            datefmt=self.DATE_FORMAT,
            level_styles=self.LEVEL_STYLES,
            field_styles=self.FIELD_STYLES
        )

        # coloredlogsの後でカスタムフォーマッターを設定
        for handler in self._logger.handlers:
            if isinstance(handler, StreamHandler) and not isinstance(handler, FileHandler):
                formatter = ColorFormat(
                    fmt=self.LOG_FORMAT,
                    datefmt=self.DATE_FORMAT,
                    level_styles=self.LEVEL_STYLES,
                    field_styles=self.FIELD_STYLES
                )
                handler.setFormatter(formatter)

    @classmethod
    def _get_caller_info(cls, depth: int = 3) -> CallerInfo:
        """呼び出し元の情報を自動取得"""
        frame = inspect.currentframe()
        try:
            if not frame:
                return "", "", 0

            for _ in range(depth):
                frame = frame.f_back
                if not frame:
                    return "", "", 0

            func_name = frame.f_code.co_qualname # クラス名付きの関数名の取得
            full_path = Path(frame.f_code.co_filename) # ファイル名を相対パスで取得
            try:
                # 現在の作業ディレクトリからの相対パスを取得
                relative_path = full_path.relative_to(Path.cwd())
                file_name = str(relative_path)
            except ValueError:
                file_name = full_path.name # 相対パスが取得できない場合はファイル名のみ

            line_no = frame.f_lineno
            return func_name, file_name, line_no

        except Exception:
            return "", "", 0
        finally:
            del frame

    @classmethod
    def _format_message(cls, msg: str, level: str, func_name: str, file_name: str, line_no: int, **kwargs: Any) -> str:
        """メッセージのフォーマット"""
        parts: list[str] = []
        location_parts: list[str] = []

        if file_name and line_no:
            location_parts.append(f"{file_name}:{line_no}")
        if func_name:
            location_parts.append(f"{func_name}")
        if location_parts:
            location_str = f"[{' > '.join(location_parts)}]"
            parts.append(f"{Color.BRIGHT_MAGENTA}{location_str}{Color.RESET}")

        kwargs_str = f"{kwargs}" if kwargs else ""
        level_upper = level.upper()
        color_code = ColorFormat.LEVEL_COLORS[level_upper]
        if level_upper in ColorFormat.LEVEL_COLORS:
            if msg and kwargs_str:
                parts.append(f"{color_code}{msg} - {kwargs_str}{Color.RESET}")
            elif msg:
                parts.append(f"{color_code}{msg}{Color.RESET}")
            elif kwargs_str:
                parts.append(f"{color_code}{kwargs_str}{Color.RESET}")
        else:
            parts.append(f"{color_code}{kwargs_str}{Color.RESET}")

        return " - ".join(parts)

    @classmethod
    def _format_json(cls, msg: str, level: str, func_name: str, file_name: str, line_no: int, exception: str, tb: str, **kwargs: Any) -> str:
        """1行の JSON にする。キーワード引数はそのまま項目にする"""
        payload: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": level.lower(),
            "message": msg,
            "file": file_name,
            "line": line_no,
            "func": func_name,
        }
        if exception:
            payload["exception"] = exception
        if tb:
            payload["traceback"] = tb
        for key, value in kwargs.items():
            payload[f"arg_{key}" if key in cls.JSON_RESERVED_KEYS else key] = value
        return json.dumps(payload, ensure_ascii=False, default=str)

    @classmethod
    def _log(cls, level: LevelName, msg: str, exc: Exception | None = None, is_traceback: bool = False, **kwargs: Any) -> None:
        """共通ログ処理（重複コード削減）"""
        if not cls._instance:
            cls()

        func_name, file_name, line_no = cls._get_caller_info()
        exception = f"{type(exc).__name__}: {str(exc)}" if exc else ""
        tb = ""
        if is_traceback:
            tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__)) if exc else traceback.format_exc()
            if tb == "NoneType: None\n":
                tb = ""

        if cls.IS_JSON:
            format_msg = cls._format_json(msg, level, func_name, file_name, line_no, exception, tb, **kwargs)
        else:
            format_msg = cls._format_message(msg, level, func_name, file_name, line_no, **kwargs)
            if exception:
                format_msg += f"\nException: {exception}"
            if tb:
                format_msg += f"\nTraceback:\n{tb}"

        if cls._instance is None:
            return

        logger = cls._instance._logger
        if not logger:
            return

        level_upper = level.upper()
        if not cls.IS_JSON and level_upper in ColorFormat.LEVEL_COLORS:
            color_code = ColorFormat.LEVEL_COLORS[level_upper]
            format_msg = f"{color_code}{format_msg}{Color.RESET}"

        match level:
            case "DEBUG":
                logger.debug(format_msg)
            case "INFO":
                logger.info(format_msg)
            case "WARNING":
                logger.warning(format_msg)
            case "ERROR":
                logger.error(format_msg)
            case "CRITICAL":
                logger.critical(format_msg)
            case _:
                assert_never(level)

    @classmethod
    def debug(cls, msg: str = "", **kwargs: Any) -> None:
        """デバッグレベルログ"""
        cls._log("DEBUG", msg, **kwargs)

    @classmethod
    def info(cls, msg: str = "", **kwargs: Any) -> None:
        """情報レベルログ"""
        cls._log("INFO", msg, **kwargs)

    @classmethod
    def warning(cls, msg: str = "", **kwargs: Any) -> None:
        """警告レベルログ"""
        cls._log("WARNING", msg, **kwargs)

    @classmethod
    def error(cls, msg: str = "", exc: Exception | None = None, **kwargs: Any) -> None:
        """エラーレベルログ（スタックトレース付き）"""
        cls._log("ERROR", msg, exc=exc, is_traceback=exc is not None, **kwargs)

    @classmethod
    def critical(cls, msg: str = "", exc: Exception | None = None, **kwargs: Any) -> None:
        """重大エラーレベルログ"""
        cls._log("CRITICAL", msg, exc=exc, is_traceback=True, **kwargs)

    @classmethod
    def set_level(cls, level: str) -> None:
        """ログレベルの動的変更"""
        if not cls._instance:
            cls()

        if level.upper() in cls.LEVEL_MAP:
            new_level = cls.LEVEL_MAP[level.upper()]
            if cls._instance is not None and cls._instance._logger:
                cls._instance._logger.setLevel(new_level)
                for handler in cls._instance._logger.handlers:
                    if isinstance(handler, StreamHandler) and not isinstance(handler, FileHandler):
                        handler.setLevel(new_level)


log = Log
