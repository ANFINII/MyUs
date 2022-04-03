import os
import ffmpeg_streaming
from ffmpeg_streaming import Formats, Bitrate, Representation, Size
from pathlib import Path


def convert_hls(video_file, path_dir, start_dir):
    """
        videos/videos_video/user_{instance.author.id}/object_{instance.id}/file_name.mp4
        videos/videos_video/user_{instance.author.id}/object_{instance.id}/file_name.m3u8
        videos/videos_video/user_{instance.author.id}/object_{instance.id}/file_name_144p.m3u8
        videos/videos_video/user_{instance.author.id}/object_{instance.id}/file_name_240p.m3u8
        videos/videos_video/user_{instance.author.id}/object_{instance.id}/file_name_360p.m3u8
        videos/videos_video/user_{instance.author.id}/object_{instance.id}/file_name_480p.m3u8
        videos/videos_video/user_{instance.author.id}/object_{instance.id}/file_name_720p.m3u8
        videos/videos_video/user_{instance.author.id}/object_{instance.id}/file_name_1080p.m3u8
    """

    # _144p  = Representation(Size(256, 144), Bitrate(95 * 1024, 64 * 1024))
    _240p  = Representation(Size(426, 240), Bitrate(150 * 1024, 94 * 1024))
    # _360p  = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
    _480p  = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
    _720p  = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
    _1080p = Representation(Size(1920, 1080), Bitrate(4096 * 1024, 320 * 1024))

    video = ffmpeg_streaming.input(video_file)
    hls = video.hls(Formats.h264())
    hls.representations(_240p, _480p, _720p, _1080p)
    hls.output(video_file)
    file_name = Path(video_file).stem
    hls_file = os.path.join(path_dir, f'{file_name}.m3u8')
    return os.path.relpath(hls_file, os.path.abspath(start_dir))


def convert_mp4(video_file, path_dir, start_dir):
    # mp4の作成 (input.mp4 -> file_name_360p.mp4)
    video = ffmpeg_streaming.input(video_file)
    _360p  = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
    hls = video.hls(Formats.h264())
    hls.representations(_360p)
    hls.output(video_file)
    return video_file
