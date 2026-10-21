from dataclasses import dataclass
from api.utils.functions.convert.audio_converter import CONVERTIBLE_EXTENSIONS


@dataclass(frozen=True, slots=True)
class UploadRuleData:
    extensions: set[str]
    content_type_prefix: str
    max_size: int


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".m4v", ".webm", ".mkv", ".avi"}
MUSIC_EXTENSIONS = {".mp3"} | CONVERTIBLE_EXTENSIONS
IMAGE_MAX_SIZE = 20 * 1024 * 1024
VIDEO_MAX_SIZE = 5 * 1024 * 1024 * 1024
MUSIC_MAX_SIZE = 500 * 1024 * 1024
