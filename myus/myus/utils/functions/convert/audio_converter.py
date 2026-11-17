import json
import math
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from ninja import UploadedFile
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from ...common.logger import log


MP3_TIMEOUT = 600
LOUDNESS_TIMEOUT = 600
TARGET_LOUDNESS = -14.0
MIN_GAIN = -20.0


def is_conversion(filename: str) -> bool:
    """MP3以外の変換対象フォーマットかチェック"""
    return Path(filename).suffix.lower() != ".mp3"


def convert_mp3(input_path: str, output_path: str, bitrate: str = "192k") -> None:
    """ffmpegで音声ファイルをMP3に変換する"""

    ffmpeg_path = shutil.which("ffmpeg") or "ffmpeg"
    cmd = [
        ffmpeg_path,
        "-protocol_whitelist", "file",
        "-i", input_path,
        "-codec:a", "libmp3lame",
        "-b:a", bitrate,
        "-ar", "44100",
        "-ac", "2",
        "-y",
        output_path,
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=MP3_TIMEOUT)
        log.info("convert completed", input_path=input_path, output_path=output_path)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        log.error("convert failed", exc=e, input_path=input_path)
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


def measure_loudness(input_path: str) -> float:
    """ffmpegで曲の大きさをLUFSで測る。測れないときは目標の大きさを返す"""

    ffmpeg_path = shutil.which("ffmpeg") or "ffmpeg"
    cmd = [
        ffmpeg_path,
        "-hide_banner",
        "-nostats",
        "-protocol_whitelist", "file",
        "-i", input_path,
        "-af", "loudnorm=print_format=json",
        "-f", "null",
        "-",
    ]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=LOUDNESS_TIMEOUT)
        stats = json.loads(result.stderr[result.stderr.rindex("{"):result.stderr.rindex("}") + 1])
        loudness = float(stats["input_i"])
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired, ValueError, KeyError) as e:
        log.warning("measure failed", exc=e, input_path=input_path)
        return TARGET_LOUDNESS

    return loudness if math.isfinite(loudness) else TARGET_LOUDNESS


def music_gain(loudness: float) -> float:
    """目標より大きい曲だけ、再生時に下げるdBを返す"""

    return round(max(MIN_GAIN, min(0.0, TARGET_LOUDNESS - loudness)), 1)


def measure_music_gain(music_path: str) -> float:
    """保存済みの曲を一時ファイルに写して測り、再生時に下げるdBを返す"""

    suffix = os.path.splitext(music_path)[1]
    try:
        with tempfile.NamedTemporaryFile(suffix=suffix) as tmp:
            with default_storage.open(music_path, "rb") as src:
                shutil.copyfileobj(src, tmp)
            tmp.flush()
            return music_gain(measure_loudness(tmp.name))
    except OSError as e:
        log.warning("read failed", exc=e, music_path=music_path)
        return 0.0
