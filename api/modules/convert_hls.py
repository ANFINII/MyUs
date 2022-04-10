import os
import ffmpeg
import ffmpeg_streaming
from ffmpeg_streaming import FFProbe, Formats, Bitrate, Representation, Size
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
        _144p  = Representation(Size(256, 144), Bitrate(95 * 1024, 64 * 1024))
        _240p  = Representation(Size(426, 240), Bitrate(150 * 1024, 94 * 1024))
        _360p  = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
        _480p  = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
        _720p  = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
        _1080p = Representation(Size(1920, 1080), Bitrate(4096 * 1024, 320 * 1024))
    """

    ffprobe = FFProbe(video_file)
    video_height = ffprobe.streams().video().get('height', 'Unknown')
    print(f'video_height: {video_height}')

    if video_height <= 360:
        _144p  = Representation(Size(256, 144), Bitrate(95 * 1024, 64 * 1024))
        _360p  = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
        video = ffmpeg_streaming.input(video_file)
        hls = video.hls(Formats.h264(), hls_time=20)
        hls.representations(_144p, _360p)

    elif video_height <= 480:
        _240p  = Representation(Size(426, 240), Bitrate(150 * 1024, 94 * 1024))
        _480p  = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
        video = ffmpeg_streaming.input(video_file)
        hls = video.hls(Formats.h264(), hls_time=20)
        hls.representations(_240p, _480p)

    elif video_height <= 720:
        _240p  = Representation(Size(426, 240), Bitrate(150 * 1024, 94 * 1024))
        _480p  = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
        _720p  = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
        video = ffmpeg_streaming.input(video_file)
        hls = video.hls(Formats.h264(), hls_time=20)
        hls.representations(_240p, _480p, _720p)

    else:
        _240p  = Representation(Size(426, 240), Bitrate(150 * 1024, 94 * 1024))
        _480p  = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
        _720p  = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
        _1080p = Representation(Size(1920, 1080), Bitrate(4096 * 1024, 320 * 1024))
        video = ffmpeg_streaming.input(video_file)
        hls = video.hls(Formats.h264(), hls_time=20)
        hls.representations(_240p, _480p, _720p, _1080p)

    hls.output(video_file)
    file_name = Path(video_file).stem
    hls_file = os.path.join(path_dir, f'{file_name}.m3u8')
    hls_file_path = os.path.relpath(hls_file, os.path.abspath(start_dir))
    return hls_file_path


def convert_mp4(video_file, path_dir, start):
    # mp4の作成 (input.mp4 -> video_360p.mp4)
    file_name = Path(video_file).stem
    stream = ffmpeg.input(video_file)
    stream = ffmpeg.hflip(stream)
    stream = ffmpeg.output(stream, f'{file_name}.mp4')
    ffmpeg.run(stream)

    file_mp4 = os.path.join(path_dir, f'{file_name}.mp4')
    path_mp4 = os.path.relpath(file_mp4, os.path.abspath(start))
    print(stream)
    print(path_mp4)
    return path_mp4
