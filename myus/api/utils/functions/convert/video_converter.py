import os
import time
import asyncio
import subprocess
from pathlib import Path
from collections.abc import Callable
from dataclasses import dataclass, field
import platform
import shutil
import psutil
from functools import lru_cache
import multiprocessing

from api.modules.logger import log


@dataclass
class OptimizedProfile:
    resolution: str
    width: int
    height: int
    bitrate: str
    max_bitrate: str
    buffer_size: str
    audio_bitrate: str
    preset: str = "p7"  # 最速プリセット
    crf: int = 25  # 少し品質を下げて速度優先
    gop_size: int = 60  # GOPサイズを増やして高速化
    threads: int = 0  # 0=auto


@dataclass
class HardwareAccelerator:
    """ハードウェアアクセラレーション設定"""
    name: str
    decoder: str | None = None
    encoder: str = "libx264"
    input_args: list[str] = field(default_factory=list)
    output_args: list[str] = field(default_factory=list)
    scale_filter: str = "scale"
    priority: int = 0  # 優先度（高いほど優先）


class VideoConverter:
    """最速動画変換クラス"""

    # 最適化プロファイル（品質と速度のバランス調整）
    PROFILES = {
        '240p': OptimizedProfile('240p', 426, 240, '350k', '500k', '700k', '48k', 'p7', 30, 60),
        '480p': OptimizedProfile('480p', 854, 480, '1200k', '1800k', '2400k', '96k', 'p7', 28, 60),
        '720p': OptimizedProfile('720p', 1280, 720, '2500k', '3750k', '5000k', '128k', 'p7', 26, 60),
        '1080p': OptimizedProfile('1080p', 1920, 1080, '5000k', '7500k', '10000k', '192k', 'p7', 25, 60),
    }

    # ハードウェアアクセラレーター定義
    ACCELERATORS = {
        'nvidia': HardwareAccelerator(
            name='NVIDIA NVENC',
            decoder='h264_cuvid',
            encoder='h264_nvenc',
            input_args=['-hwaccel', 'cuda', '-hwaccel_output_format', 'cuda', '-hwaccel_device', '0'],
            output_args=[
                '-rc', 'vbr',
                '-rc-lookahead', '16',  # 低減して高速化
                '-temporal-aq', '1',
                '-spatial-aq', '1',
                '-aq-strength', '6',  # 低減
                '-b_ref_mode', 'disabled',  # 無効化して高速化
                '-dpb_size', '2',  # 低減
                '-refs', '2',  # 参照フレーム削減
                '-bf', '0',  # Bフレーム無効化
            ],
            scale_filter='scale_cuda',
            priority=100
        ),
        'videotoolbox': HardwareAccelerator(
            name='Apple VideoToolbox',
            decoder='h264',
            encoder='h264_videotoolbox',
            input_args=['-hwaccel', 'videotoolbox'],
            output_args=[
                '-realtime', '1',  # リアルタイムモード
                '-compression_level', '0.5',  # 圧縮レベル下げる
                '-max_slice_bytes', '-1',
                '-allow_sw', '1',
                '-prio_speed', '1',  # 速度優先
            ],
            scale_filter='scale',
            priority=90
        ),
        'qsv': HardwareAccelerator(
            name='Intel Quick Sync',
            decoder='h264_qsv',
            encoder='h264_qsv',
            input_args=['-hwaccel', 'qsv', '-hwaccel_output_format', 'qsv', '-qsv_device', '/dev/dri/renderD128'],
            output_args=[
                '-preset', 'veryfast',
                '-look_ahead', '0',  # 無効化
                '-async_depth', '4',  # 非同期深度
                '-g', '120',  # GOPサイズ増加
            ],
            scale_filter='scale_qsv',
            priority=80
        ),
        'amf': HardwareAccelerator(
            name='AMD AMF',
            decoder='h264',
            encoder='h264_amf',
            input_args=[],
            output_args=[
                '-quality', 'speed',
                '-rc', 'vbr_peak',
                '-preanalysis', 'false',  # 無効化して高速化
                '-b_frame_delta_qp', '4',
                '-ref_b_frame_delta_qp', '4',
            ],
            scale_filter='scale',
            priority=70
        ),
    }

    def __init__(self, force_cpu: bool = False, max_parallel_gpus: int = 8):
        """
        初期化

        Args:
            force_cpu: CPU処理を強制
            max_parallel_gpus: GPU並列処理の最大数
        """
        self.force_cpu = force_cpu
        self.max_parallel_gpus = max_parallel_gpus
        self.ffmpeg_path = shutil.which('ffmpeg') or 'ffmpeg'
        self.ffprobe_path = shutil.which('ffprobe') or 'ffprobe'
        self.available_accelerators = self._detect_hardware_accelerators() # ハードウェア検出
        self.optimal_workers = self._calculate_optimal_workers() # 最適な並列数を計算（増加）
        self._gpu_semaphore = asyncio.Semaphore(max_parallel_gpus) # GPU使用カウンター（複数GPU対応）

        # CPU使用セマフォ（CPUコア数に基づく）
        cpu_cores = multiprocessing.cpu_count()
        self._cpu_semaphore = asyncio.Semaphore(cpu_cores)

    def _detect_hardware_accelerators(self) -> list[HardwareAccelerator]:
        """利用可能なハードウェアアクセラレーターを検出"""
        if self.force_cpu:
            return []

        available = []

        # NVIDIA GPU
        if self._check_nvidia_gpu():
            available.append(self.ACCELERATORS['nvidia'])

        # macOS VideoToolbox
        if platform.system() == 'Darwin':
            available.append(self.ACCELERATORS['videotoolbox'])

        # Intel QSV
        if self._check_intel_qsv():
            available.append(self.ACCELERATORS['qsv'])

        # AMD AMF
        if platform.system() == 'Windows' and self._check_amd_gpu():
            available.append(self.ACCELERATORS['amf'])

        # 優先度でソート
        available.sort(key=lambda x: x.priority, reverse=True)

        if available:
            log.info(f"検出されたアクセラレーター: {[a.name for a in available]}")
        else:
            log.info("ハードウェアアクセラレーターなし、CPU処理を使用")

        return available

    def _check_nvidia_gpu(self) -> bool:
        """NVIDIA GPU検出"""
        try:
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv,noheader'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                gpu_info = result.stdout.strip()
                log.info(f"NVIDIA GPU検出: {gpu_info}")

                # NVENCサポート確認
                nvenc_check = subprocess.run(
                    [self.ffmpeg_path, '-hide_banner', '-encoders'],
                    capture_output=True,
                    text=True
                )
                if 'h264_nvenc' in nvenc_check.stdout:
                    return True

        except FileNotFoundError:
            pass  # NVIDIA GPUなし
        except Exception:
            pass  # エラー時はスキップ

        return False

    def _check_intel_qsv(self) -> bool:
        """Intel QSV検出"""
        try:
            # QSVエンコーダー確認
            result = subprocess.run(
                [self.ffmpeg_path, '-hide_banner', '-encoders'],
                capture_output=True,
                text=True
            )
            return 'h264_qsv' in result.stdout
        except Exception:
            log.critical("Intel GPU検出エラー")
            return False

    def _check_amd_gpu(self) -> bool:
        """AMD GPU検出"""
        try:
            # Windows WMI経由でGPU情報取得
            if platform.system() == 'Windows':
                try:
                    import wmi
                    c = wmi.WMI()
                    for gpu in c.Win32_VideoController():
                        if 'AMD' in gpu.Name or 'Radeon' in gpu.Name:
                            return True
                except ImportError:
                    log.debug("wmi module not available")
        except Exception:
            log.critical("AMD GPU detection error")
        return False

    def _calculate_optimal_workers(self) -> int:
        """最適な並列処理数を計算（改善版）"""
        cpu_count = os.cpu_count() or 4
        memory_gb = psutil.virtual_memory().total / (1024**3)
        memory_limited_workers = int(memory_gb / 1.5) # メモリ制約（1プロセスあたり1.5GB想定）
        cpu_limited_workers = int(cpu_count * 1.5) # CPU制約（コア数の1.5倍まで）

        # GPU使用時はより多くの並列処理
        if self.available_accelerators:
            cpu_limited_workers = min(cpu_limited_workers, 12)

        optimal = min(memory_limited_workers, cpu_limited_workers, 16)
        log.info(f"最適並列数: {optimal} (CPU: {cpu_count}, Memory: {memory_gb:.1f}GB)")

        return max(optimal, 4)

    @lru_cache(maxsize=64)
    def _get_video_metadata(self, input_path: str) -> dict:
        """動画メタデータ取得（キャッシュ付き）"""
        cmd = [
            self.ffprobe_path,
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            input_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise ValueError(f"動画情報取得失敗: {input_path}")

        import json
        return json.loads(result.stdout)

    def _build_command(
        self,
        input_path: str,
        output_path: str,
        profile: OptimizedProfile,
        segment_pattern: str,
        accelerator: HardwareAccelerator | None = None
    ) -> list[str]:
        """超高速変換コマンド構築（最適化版）"""

        cmd = [self.ffmpeg_path, '-hide_banner', '-loglevel', 'error', '-stats']
        # 入力設定（最適化）
        if accelerator:
            cmd.extend(accelerator.input_args)

        # 入力バッファサイズとスレッド設定
        cmd.extend([
            '-thread_queue_size', '4096',  # 入力キューサイズ増加
            '-i', input_path,
            '-y',
            '-map', '0:v:0',  # 最初のビデオストリームのみ
            '-map', '0:a:0?',  # 最初のオーディオストリーム（あれば）
        ])

        # スケーリングフィルター（最適化）
        if accelerator and accelerator.scale_filter != 'scale':
            scale_filter = f"{accelerator.scale_filter}={profile.width}:{profile.height}:force_original_aspect_ratio=decrease"

            # NVIDIAの場合は高速補間
            if 'cuda' in accelerator.scale_filter:
                scale_filter += ":interp_algo=bilinear"  # より高速
        else:
            scale_filter = f"scale={profile.width}:{profile.height}:force_original_aspect_ratio=decrease:flags=bilinear"  # 高速

        cmd.extend(['-vf', scale_filter]) # パディング処理を簡略化
        encoder = accelerator.encoder if accelerator else 'libx264' # ビデオエンコーダー設定
        cmd.extend(['-c:v', encoder])

        # ビットレート設定（シンプル化）
        cmd.extend([
            '-b:v', profile.bitrate,
            '-maxrate', profile.max_bitrate,
            '-bufsize', profile.buffer_size,
        ])

        # エンコーダー固有設定（最適化）
        if accelerator:
            if 'nvenc' in encoder:
                cmd.extend([
                    '-preset', profile.preset,
                    '-profile:v', 'baseline',  # 互換性と速度優先
                    '-level', '4.0',
                    '-cq', str(profile.crf + 2),  # 品質を少し下げる
                    '-weighted_pred', '0',  # 無効化
                    '-nonref_p', '1',  # 非参照Pフレーム使用
                ])
            elif 'videotoolbox' in encoder:
                cmd.extend([
                    '-profile:v', 'baseline',
                    '-level', '4.0',
                ])
            cmd.extend(accelerator.output_args)
        else:
            # CPU (x264)超高速設定
            cmd.extend([
                '-preset', 'ultrafast',  # 最速プリセット
                '-tune', 'fastdecode',  # デコード最適化
                '-profile:v', 'baseline',  # シンプルなプロファイル
                '-level', '4.0',
                '-crf', str(profile.crf + 2),
                '-x264-params', f'threads={profile.threads}:lookahead_threads=2:sliced_threads=1:ref=1:me=dia:subme=0:bframes=0:b-adapt=0:mixed-refs=0:trellis=0:weightp=0:scenecut=0:no-deblock=1',
            ])

        # GOP設定（HLS用、増加）
        cmd.extend([
            '-g', str(profile.gop_size),
            '-keyint_min', str(profile.gop_size),
            '-sc_threshold', '0',
        ])

        # オーディオ設定（超高速化）
        cmd.extend([
            '-c:a', 'aac',
            '-b:a', profile.audio_bitrate,
            '-ar', '44100',
            '-ac', '2',
            '-aac_coder', 'fast',  # 高速AACエンコーダー
        ])

        # HLS出力設定（最適化）
        cmd.extend([
            '-f', 'hls',
            '-hls_time', '6',  # セグメント時間を増やす
            '-hls_list_size', '0',
            '-hls_segment_type', 'mpegts',
            '-hls_flags', 'independent_segments',  # temp_file削除して高速化
            '-hls_playlist_type', 'vod',
            '-hls_segment_filename', segment_pattern,
            '-threads', '0',  # 自動最適化
            output_path
        ])

        return cmd

    async def _convert_single_resolution_async(
        self,
        input_path: str,
        output_dir: str,
        profile: OptimizedProfile,
        accelerator: HardwareAccelerator | None = None,
        progress_callback: Callable[[float], None] | None = None
    ) -> tuple[str, float, dict]:
        """非同期単一解像度変換（最適化版）"""

        start_time = time.time()
        stats = {'encoder': 'cpu', 'gpu_used': False}
        base_name = Path(input_path).stem
        output_path = os.path.join(output_dir, f"{base_name}_{profile.resolution}.m3u8")
        segment_pattern = os.path.join(output_dir, f"{base_name}_{profile.resolution}_%05d.ts")

        # リソース制限（GPU/CPU）
        resource_lock = None
        if accelerator:
            resource_lock = await self._gpu_semaphore.acquire()
            stats['encoder'] = accelerator.encoder
            stats['gpu_used'] = True
        else:
            resource_lock = await self._cpu_semaphore.acquire()

        try:
            cmd = self._build_command(input_path, output_path, profile, segment_pattern, accelerator)

            # 非同期実行（優先度設定）
            if platform.system() != 'Windows':
                # Unix系の場合、nice値を設定
                cmd = ['nice', '-n', '-5'] + cmd

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.DEVNULL,  # エラー出力を無視して高速化
                limit=1024*1024*10  # バッファサイズ増加
            )

            # 非ブロッキング待機
            await process.wait()

            if process.returncode != 0:
                # エラーでも続行（部分的な成功を許容）
                log.warning(f"変換警告: {profile.resolution}")

            elapsed = time.time() - start_time
            stats['time'] = elapsed

            if progress_callback:
                await progress_callback(profile.resolution, elapsed)

            return profile.resolution, elapsed, stats

        finally:
            if accelerator and resource_lock:
                self._gpu_semaphore.release()
            elif not accelerator and resource_lock:
                self._cpu_semaphore.release()

    async def convert_async(
        self,
        input_path: str,
        output_dir: str,
        resolutions: list[str] | None = None,
        progress_callback: Callable[[float], None] | None = None
    ) -> dict:
        """超高速非同期並列変換"""

        start_time = time.time()
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # メタデータ取得（キャッシュ済み）
        metadata = self._get_video_metadata(input_path)
        video_stream = next((s for s in metadata['streams'] if s['codec_type'] == 'video'), None)

        if not video_stream:
            raise ValueError("ビデオストリームが見つかりません")

        original_height = int(video_stream.get('height', 0))

        # 変換解像度決定（最適化）
        if resolutions is None:
            resolutions = []
            for res, profile in self.PROFILES.items():
                if profile.height <= original_height:
                    resolutions.append(res)
                if profile.height >= original_height * 1.2:  # 1.2倍で打ち切り
                    break

        # 変換タスク作成（並列度増加）
        tasks = []
        profiles = [self.PROFILES[res] for res in resolutions if res in self.PROFILES]

        # アクセラレーター割り当て（改善版）
        if self.available_accelerators:
            # GPUがある場合、全解像度をGPUで処理
            for profile in profiles:
                accelerator = self.available_accelerators[0]
                task = self._convert_single_resolution_async(
                    input_path,
                    output_dir,
                    profile,
                    accelerator,
                    progress_callback
                )
                tasks.append(task)
        else:
            # CPUの場合も並列処理
            for profile in profiles:
                task = self._convert_single_resolution_async(
                    input_path,
                    output_dir,
                    profile,
                    None,
                    progress_callback
                )
                tasks.append(task)

        # 並列実行（タイムアウト付き）
        try:
            results = await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True),
                timeout=300  # 5分タイムアウト
            )
        except asyncio.TimeoutError:
            log.warning("変換タイムアウト")
            results = []

        # 結果集計
        conversion_stats = {
            'resolutions': {},
            'total_time': time.time() - start_time,
            'hardware_used': {},
            'errors': []
        }

        for result in results:
            if isinstance(result, Exception):
                conversion_stats['errors'].append(str(result))
            else:
                resolution, elapsed, stats = result
                conversion_stats['resolutions'][resolution] = {
                    'time': elapsed,
                    'encoder': stats['encoder'],
                    'gpu_used': stats['gpu_used']
                }

                # ハードウェア使用統計
                encoder = stats['encoder']
                if encoder not in conversion_stats['hardware_used']:
                    conversion_stats['hardware_used'][encoder] = 0
                conversion_stats['hardware_used'][encoder] += 1

        # 成功した解像度のリスト
        successful_resolutions = [r for r in resolutions if r in conversion_stats['resolutions']]
        base_name = Path(input_path).stem

        # HLSマスタープレイリスト生成（簡略化）
        if successful_resolutions:
            self._create_master_playlist(
                base_name,
                successful_resolutions,
                output_dir
            )
            conversion_stats['hls_path'] = os.path.join(output_dir, f"{base_name}_master.m3u8")
        else:
            conversion_stats['hls_path'] = None

        # MP4生成（高速版）
        try:
            mp4_path = await self._create_mp4_file(
                input_path,
                output_dir,
                base_name,
                successful_resolutions
            )
            conversion_stats['mp4_path'] = mp4_path
        except Exception:
            log.critical("MP4生成エラー")
            conversion_stats['mp4_path'] = None

        return conversion_stats

    async def _create_mp4_file(
        self,
        input_path: str,
        output_dir: str,
        base_name: str,
        available_resolutions: list[str]
    ) -> str:
        """高速MP4ファイル生成"""

        # 480p優先、なければ最低解像度
        target_resolution = '480p' if '480p' in available_resolutions else (
            sorted(available_resolutions, key=lambda x: int(x.rstrip('p')))[0]
            if available_resolutions else None
        )

        if not target_resolution:
            mp4_path = os.path.join(output_dir, f"{base_name}_convert.mp4")
            if os.path.abspath(input_path) != os.path.abspath(mp4_path):
                shutil.copy2(input_path, mp4_path)
                return mp4_path
            return input_path

        profile = self.PROFILES[target_resolution]
        mp4_path = os.path.join(output_dir, f"{base_name}_convert.mp4")

        # 超高速MP4変換コマンド
        cmd = [
            self.ffmpeg_path,
            '-i', input_path,
            '-y',
            '-vf', f"scale={profile.width}:{profile.height}:force_original_aspect_ratio=decrease",
            '-c:v', 'libx264',
            '-preset', 'ultrafast',  # 最速
            '-crf', '28',  # 品質下げて高速化
            '-c:a', 'copy',  # オーディオコピーで高速化
            '-movflags', '+faststart',
            mp4_path
        ]

        # 非同期実行
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL
        )
        await process.wait()

        if process.returncode != 0:
            # エラー時は元ファイルコピー
            if os.path.abspath(input_path) != os.path.abspath(mp4_path):
                shutil.copy2(input_path, mp4_path)

        return mp4_path

    def _create_master_playlist(
        self,
        base_name: str,
        resolutions: list[str],
        output_dir: str
    ) -> None:
        """マスタープレイリスト生成"""

        master_path = os.path.join(output_dir, f"{base_name}_master.m3u8")
        content = "#EXTM3U\n#EXT-X-VERSION:3\n\n"

        for res in resolutions:
            if res not in self.PROFILES:
                continue

            profile = self.PROFILES[res]
            video_bandwidth = int(profile.max_bitrate.rstrip('k')) * 1000
            audio_bandwidth = int(profile.audio_bitrate.rstrip('k')) * 1000
            total_bandwidth = video_bandwidth + audio_bandwidth

            content += (
                f'#EXT-X-STREAM-INF:BANDWIDTH={total_bandwidth},'
                f'RESOLUTION={profile.width}x{profile.height}\n'
                f'{base_name}_{res}.m3u8\n\n'
            )

        with open(master_path, 'w', encoding='utf-8') as f:
            f.write(content)

        log.info(f"マスタープレイリスト生成: {master_path}")

    def transcode(
        self,
        input_path: str,
        output_dir: str,
        resolutions: list[str] | None = None,
        progress_callback: Callable[[float], None] | None = None
    ) -> dict:
        """同期インターフェース（後方互換性）"""
        return asyncio.run(self.convert_async(input_path, output_dir, resolutions, progress_callback))
