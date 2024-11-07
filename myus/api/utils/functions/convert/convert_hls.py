import os
import ffmpeg_streaming

from ffmpeg_streaming import FFProbe, Formats, Bitrate, Representation, Size
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from myus.api.utils.functions.convert.master_m3u8 import Masterm3u8

# from ffmpeg_streaming import  S3, CloudManager
# s3 = S3(aws_access_key_id='YOUR_KEY_ID', aws_secret_access_key='YOUR_KEY_SECRET', region_name='YOUR_REGION')
# save_to_s3 = CloudManager().add(s3, bucket_name="bucket-name")
# hls.output(clouds=save_to_s3)


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


def thread_hls(video_file, convert, resolution):
    video = ffmpeg_streaming.input(video_file)
    hls = video.hls(Formats.h264(), hls_time=20)
    hls.representations(convert,)
    hls.output(video_file)
    print(f'{resolution}_hls: {video_file}')


def thread_mp4(video_file, path_dir, resolution):
    file_name = Path(video_file).stem
    video = ffmpeg_streaming.input(f'{path_dir}/{file_name}_{resolution}.m3u8')
    stream = video.stream2file(Formats.h264())
    stream.output(f'{path_dir}/{file_name}.mp4')
    print(f'{resolution}_mp4: {video_file}')


def convert_exe(video_file, path_dir, start_dir):
    ffprobe = FFProbe(video_file)
    file_name = Path(video_file).stem
    video_height = ffprobe.streams().video().get('height', 'unknown')
    print(f'file_name: {file_name}, video_height: {video_height}')

    _144p  = Representation(Size(256, 144), Bitrate(95 * 1024, 64 * 1024))
    _240p  = Representation(Size(426, 240), Bitrate(150 * 1024, 94 * 1024))
    _360p  = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
    _480p  = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
    _720p  = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
    _1080p = Representation(Size(1920, 1080), Bitrate(4096 * 1024, 320 * 1024))

    if video_height <= 360:
        with ProcessPoolExecutor(max_workers=2) as exe:
            exe.submit(thread_hls, video_file, _144p, '144p')
            exe.submit(thread_hls, video_file, _360p, '360p')
        master = Masterm3u8.master_360p(file_name)
        thread_mp4(video_file, path_dir, '360p')
    elif video_height <= 480:
        with ProcessPoolExecutor(max_workers=2) as exe:
            exe.submit(thread_hls, video_file, _240p, '240p')
            exe.submit(thread_hls, video_file, _480p, '480p')
        master = Masterm3u8.master_480p(file_name)
        thread_mp4(video_file, path_dir, '480p')
    elif video_height <= 720:
        with ProcessPoolExecutor(max_workers=3) as exe:
            exe.submit(thread_hls, video_file, _240p, '240p')
            exe.submit(thread_hls, video_file, _480p, '480p')
            exe.submit(thread_hls, video_file, _720p, '720p')
        master = Masterm3u8.master_720p(file_name)
        thread_mp4(video_file, path_dir, '480p')
    else:
        with ProcessPoolExecutor(max_workers=4) as exe:
            exe.submit(thread_hls, video_file, _240p, '240p')
            exe.submit(thread_hls, video_file, _480p, '480p')
            exe.submit(thread_hls, video_file, _720p, '720p')
            exe.submit(thread_hls, video_file, _1080p, '1080p')
        master = Masterm3u8.master_1080p(file_name)
        thread_mp4(video_file, path_dir, '480p')

    hls_file = os.path.join(path_dir, f'{file_name}.m3u8')
    hls_path = os.path.relpath(hls_file, os.path.abspath(start_dir))
    mp4_file = os.path.join(path_dir, f'{file_name}.mp4')
    mp4_path = os.path.relpath(mp4_file, os.path.abspath(start_dir))
    f = open(hls_file, 'w')
    f.write(master)
    f.close()
    return {'hls_path': hls_path, 'mp4_path': mp4_path}
