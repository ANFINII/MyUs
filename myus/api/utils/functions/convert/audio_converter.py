import shutil
import subprocess
import os
import tempfile
from pathlib import Path
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from ninja import UploadedFile
from api.modules.logger import log


CONVERTIBLE_EXTENSIONS = {".wav", ".flac", ".ogg", ".m4a", ".aac", ".wma", ".aiff"}


def is_conversion(filename: str) -> bool:
    """MP3以外の変換対象フォーマットかチェック"""
    return Path(filename).suffix.lower() in CONVERTIBLE_EXTENSIONS


def convert_mp3(input_path: str, output_path: str, bitrate: str = "192k") -> None:
    """ffmpegで音声ファイルをMP3に変換する"""

    ffmpeg_path = shutil.which("ffmpeg") or "ffmpeg"
    cmd = [
        ffmpeg_path,
        "-i", input_path,
        "-codec:a", "libmp3lame",
        "-b:a", bitrate,
        "-ar", "44100",
        "-ac", "2",
        "-y",
        output_path,
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        log.info("MP3変換完了", input_path=input_path, output_path=output_path)
    except subprocess.CalledProcessError as e:
        log.error("MP3変換エラー", exc=e, input_path=input_path)
        raise


def save_converted_mp3(file: UploadedFile, path: str) -> str:
    """音声ファイルをMP3に変換して保存する"""

    suffix = os.path.splitext(file.name or "upload")[1]
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp_in:
        for chunk in file.chunks():
            tmp_in.write(chunk)
        tmp_in_path = tmp_in.name

    tmp_out_path = tmp_in_path.rsplit(".", 1)[0] + ".mp3"
    try:
        convert_mp3(tmp_in_path, tmp_out_path)
        with open(tmp_out_path, "rb") as f:
            return default_storage.save(path, ContentFile(f.read()))
    finally:
        os.unlink(tmp_in_path)
        if os.path.exists(tmp_out_path):
            os.unlink(tmp_out_path)
