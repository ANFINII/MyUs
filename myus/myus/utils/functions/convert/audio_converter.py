import json
import math
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from django.core.files import File
from django.core.files.storage import default_storage
from ...common.logger import log


MIN_BIT_RATE = 180000
MIN_GAIN = -20.0
TARGET_LOUDNESS = -14.0
PROBE_TIMEOUT = 60
LOUDNESS_TIMEOUT = 600
MP3_TIMEOUT = 600
MP3_BITRATE = "320k"


@dataclass(frozen=True, slots=True)
class AudioInfo:
    codec: str
    bit_rate: int
    sample_rate: int
    bit_depth: int
    duration: float


@dataclass(frozen=True, slots=True)
class AudioConvert:
    audio: str
    gain: float


def is_conversion(filename: str) -> bool:
    """MP3以外の変換対象フォーマットかチェック"""
    return Path(filename).suffix.lower() != ".mp3"


def probe_audio(path: str) -> AudioInfo:
    """ffprobeで最初の音声の形式・ビットレート・サンプリングレート・ビット深度・長さを読む。読めないときは空の形式と0を返す"""

    ffprobe_path = shutil.which("ffprobe") or "ffprobe"
    cmd = [ffprobe_path, "-v", "error", "-protocol_whitelist", "file", "-select_streams", "a:0", "-show_entries", "stream=codec_name,bit_rate,sample_rate,bits_per_raw_sample:format=bit_rate,duration", "-of", "json", path]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=PROBE_TIMEOUT)
        probe = json.loads(result.stdout)
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as e:
        log.warning("probe failed", exc=e, path=path)
        return AudioInfo(codec="", bit_rate=0, sample_rate=0, bit_depth=0, duration=0.0)

    streams = probe.get("streams") or [{}]
    stream = streams[0]
    bit_rate = stream.get("bit_rate") or probe.get("format", {}).get("bit_rate")
    return AudioInfo(
        codec=str(stream.get("codec_name", "")),
        bit_rate=probe_int(bit_rate),
        sample_rate=probe_int(stream.get("sample_rate")),
        bit_depth=probe_int(stream.get("bits_per_raw_sample")),
        duration=probe_float(probe.get("format", {}).get("duration")),
    )


def probe_int(value: object) -> int:
    text = str(value)
    return int(text) if text.isdigit() else 0


def probe_float(value: object) -> float:
    try:
        return float(str(value))
    except ValueError:
        return 0.0


def is_lossless(codec: str) -> bool:
    return codec == "flac" or codec.startswith("pcm_")


def is_low_bit_rate(audio: AudioInfo) -> bool:
    """音を削る形式で、ビットレートが分かり、180kbps より低いか"""
    return not is_lossless(audio.codec) and 0 < audio.bit_rate < MIN_BIT_RATE


def convert_mp3(input_path: str, output_path: str, bitrate: str = MP3_BITRATE) -> None:
    """ffmpegでオーディオファイルをMP3に変換する"""

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


def audio_gain(loudness: float) -> float:
    """目標より大きい曲だけ、再生時に下げるdBを返す"""

    return round(max(MIN_GAIN, min(0.0, TARGET_LOUDNESS - loudness)), 1)


def convert_audio(audio_path: str) -> AudioConvert:
    """保存済みの曲を一時フォルダに取り出し、MP3以外はMP3に変換して保存先に上げ、MP3の相対パスと再生時に下げるdBを返す。音質が低いときや変換できないときは空のパスを返す"""

    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_path = os.path.join(tmp_dir, os.path.basename(audio_path))
            with default_storage.open(audio_path, "rb") as src, open(input_path, "wb") as dst:
                shutil.copyfileobj(src, dst)

            audio = probe_audio(input_path)
            if is_low_bit_rate(audio):
                log.warning("low bit rate", audio_path=audio_path, codec=audio.codec, bit_rate=audio.bit_rate)
                return AudioConvert(audio="", gain=0.0)

            if not is_conversion(audio_path):
                return AudioConvert(audio=audio_path, gain=audio_gain(measure_loudness(input_path)))

            output_path = os.path.join(tmp_dir, "convert.mp3")
            convert_mp3(input_path, output_path)
            with open(output_path, "rb") as f:
                save_path = default_storage.save(os.path.splitext(audio_path)[0] + ".mp3", File(f))
            return AudioConvert(audio=save_path, gain=audio_gain(measure_loudness(output_path)))
    except Exception as e:
        log.error("convert failed", exc=e, audio_path=audio_path)
        return AudioConvert(audio="", gain=0.0)
