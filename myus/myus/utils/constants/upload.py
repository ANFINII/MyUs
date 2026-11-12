from dataclasses import dataclass
from ..functions.convert.audio_converter import CONVERTIBLE_EXTENSIONS


@dataclass(frozen=True, slots=True)
class UploadRuleData:
    extensions: set[str]
    content_type_prefix: str
    max_size: int


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
IMAGE_FORMATS = {"JPEG", "PNG", "GIF", "WEBP"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".m4v", ".webm", ".mkv", ".avi"}
MUSIC_EXTENSIONS = {".mp3"} | CONVERTIBLE_EXTENSIONS
VIDEO_FORMATS = {"mov", "mp4", "m4a", "3gp", "3g2", "mj2", "matroska", "webm", "avi"}
MUSIC_FORMATS = {"mp3", "wav", "flac", "ogg", "mov", "mp4", "m4a", "3gp", "3g2", "mj2", "aac", "asf", "aiff"}
IMAGE_MAX_SIZE = 20 * 1024 * 1024
VIDEO_MAX_SIZE = 5 * 1024 * 1024 * 1024
MUSIC_MAX_SIZE = 500 * 1024 * 1024
