import json
import os
import time
import datetime
from pathlib import Path
from typing import Any

from django.conf import settings
from api.utils.functions.convert.video_converter import VideoConverter
from api.modules.logger import log


def encode_video(convert_path: str, output_dir: str, save_log: bool = True) -> dict[str, Any]:
    """
    動画をエンコードして統計情報を返す

    Args:
        convert_path: 変換元の動画ファイルパス
        output_dir: 出力先ディレクトリ
        save_log: エンコード履歴をログファイルに保存するか

    Returns:
        エンコード統計情報の辞書

    Raises:
        ValueError: ファイルが存在しない場合や変換に失敗した場合
    """
    # ファイル存在チェック
    if not os.path.exists(convert_path):
        raise ValueError(f"Video file not found: {convert_path}")

    # エンコード開始時刻を記録
    encode_start_time = time.time()
    log.info(
        "========== エンコード開始 ==========",
        name=os.path.basename(convert_path),
        size=f"{os.path.getsize(convert_path) / 1024 / 1024:.2f} MB",
        start_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(encode_start_time))
    )

    # 動画変換実行
    converter = VideoConverter()
    conversion_stats = converter.transcode(input_path=convert_path, output_dir=output_dir, resolutions=None)

    # エンコード終了時刻を記録
    encode_end_time = time.time()
    encode_duration = encode_end_time - encode_start_time

    log.info(
        "========== エンコード完了 ==========",
        end_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(encode_end_time)),
        duration_sec=f"{encode_duration:.2f}秒",
        duration_min=f"{encode_duration/60:.2f}分",
        resolutions=list(conversion_stats.get('resolutions', {}).keys())
    )

    # 各解像度の処理時間
    log.info("--- 解像度別処理時間 ---")
    if 'resolutions' in conversion_stats:
        for res, info in conversion_stats['resolutions'].items():
            log.info(f"  {res}: {info.get('time', 0):.2f}秒 (エンコーダ: {info.get('encoder', 'unknown')})")

    log.info(f"ハードウェア使用統計: {conversion_stats.get('hardware_used', {})}")

    if save_log:
        save_encoding_log(convert_path, encode_duration, conversion_stats)

    # 統計情報に処理時間を追加
    conversion_stats.update({
        'encode_duration': encode_duration,
        'encode_start_time': encode_start_time,
        'encode_end_time': encode_end_time
    })

    return conversion_stats


def save_encoding_log(convert_path: str, encode_duration: float, conversion_stats: dict[str, Any]) -> None:
    """
    エンコード履歴をログファイルに保存

    Args:
        convert_path: 変換元の動画ファイルパス
        encode_duration: エンコード処理時間（秒）
        conversion_stats: 変換統計情報
    """
    # logsディレクトリの作成
    log_dir = Path(settings.BASE_DIR) / "logs"
    log_dir.mkdir(exist_ok=True)
    encoding_log_file = log_dir / f"video_encoding_{datetime.datetime.now().strftime('%Y%m')}.log"

    # 詳細なログエントリを作成
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "filename": os.path.basename(convert_path),
        "filesize_mb": round(os.path.getsize(convert_path) / 1024 / 1024, 2),
        "duration_sec": round(encode_duration, 2),
        "resolutions": list(conversion_stats.get('resolutions', {}).keys()),
        "resolution_details": conversion_stats.get('resolutions', {}),
        "hardware_used": conversion_stats.get('hardware_used', {}),
        "gpu_used": conversion_stats.get('gpu_used', False),
        "errors": conversion_stats.get('errors', [])
    }

    try:
        with open(encoding_log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        log.info(f"エンコード履歴を保存: {encoding_log_file}")
    except Exception as e:
        log.error("エンコード履歴の保存エラー", exc=e)
