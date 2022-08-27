import os
import ffmpeg_streaming

from ffmpeg_streaming import FFProbe, Formats, Bitrate, Representation, Size
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from apps.myus.convert.master_m3u8 import Masterm3u8

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
    _144p  = Representation(Size(256, 144), Bitrate(95 * 1024, 64 * 1024))
    _240p  = Representation(Size(426, 240), Bitrate(150 * 1024, 94 * 1024))
    _360p  = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
    _480p  = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
    _720p  = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
    _1080p = Representation(Size(1920, 1080), Bitrate(4096 * 1024, 320 * 1024))
"""


def thread_144p(video_file):
    _144p = Representation(Size(256, 144), Bitrate(95 * 1024, 64 * 1024))
    video = ffmpeg_streaming.input(video_file)
    hls = video.hls(Formats.h264(), hls_time=20)
    hls.representations(_144p,)
    hls.output(video_file)
    print(f'thread_144p: {video_file}')

def thread_240p(video_file):
    _240p = Representation(Size(426, 240), Bitrate(150 * 1024, 94 * 1024))
    video = ffmpeg_streaming.input(video_file)
    hls = video.hls(Formats.h264(), hls_time=20)
    hls.representations(_240p,)
    hls.output(video_file)
    print(f'thread_240p: {video_file}')

def thread_360p(video_file):
    _360p = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
    video = ffmpeg_streaming.input(video_file)
    hls = video.hls(Formats.h264(), hls_time=20)
    hls.representations(_360p,)
    hls.output(video_file)
    print(f'thread_360p: {video_file}')

def thread_480p(video_file):
    _480p = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
    video = ffmpeg_streaming.input(video_file)
    hls = video.hls(Formats.h264(), hls_time=20)
    hls.representations(_480p,)
    hls.output(video_file)
    print(f'thread_480p: {video_file}')

def thread_720p(video_file):
    _720p = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
    video = ffmpeg_streaming.input(video_file)
    hls = video.hls(Formats.h264(), hls_time=20)
    hls.representations(_720p,)
    hls.output(video_file)
    print(f'thread_720p: {video_file}')

def thread_1080p(video_file):
    _1080p = Representation(Size(1920, 1080), Bitrate(4096 * 1024, 320 * 1024))
    video = ffmpeg_streaming.input(video_file)
    hls = video.hls(Formats.h264(), hls_time=20)
    hls.representations(_1080p,)
    hls.output(video_file)
    print(f'thread_1080p: {video_file}')

def convert_360p_mp4(video_file, path_dir):
    file_name = Path(video_file).stem
    video = ffmpeg_streaming.input(f'{path_dir}/{file_name}_360p.m3u8')
    stream = video.stream2file(Formats.h264())
    stream.output(f'{path_dir}/{file_name}.mp4')
    print(f'convert_360p_mp4: {video_file}')

def convert_480p_mp4(video_file, path_dir):
    file_name = Path(video_file).stem
    video = ffmpeg_streaming.input(f'{path_dir}/{file_name}_480p.m3u8')
    stream = video.stream2file(Formats.h264())
    stream.output(f'{path_dir}/{file_name}.mp4')
    print(f'convert_480p_mp4: {video_file}')

def convert_hls(video_file, path_dir, start_dir):
    ffprobe = FFProbe(video_file)
    file_name = Path(video_file).stem
    video_height = ffprobe.streams().video().get('height', 'unknown')
    print(f'file_name: {file_name}, video_height: {video_height}')

    if video_height <= 360:
        with ProcessPoolExecutor(max_workers=2) as exe:
            exe.submit(thread_144p, video_file)
            exe.submit(thread_360p, video_file)
        master = Masterm3u8.master_360p(file_name)
        convert_360p_mp4(video_file, path_dir)
    elif video_height <= 480:
        with ProcessPoolExecutor(max_workers=2) as exe:
            exe.submit(thread_240p, video_file)
            exe.submit(thread_480p, video_file)
        master = Masterm3u8.master_480p(file_name)
        convert_480p_mp4(video_file, path_dir)
    elif video_height <= 720:
        with ProcessPoolExecutor(max_workers=3) as exe:
            exe.submit(thread_240p, video_file)
            exe.submit(thread_480p, video_file)
            exe.submit(thread_720p, video_file)
        master = Masterm3u8.master_720p(file_name)
        convert_480p_mp4(video_file, path_dir)
    else:
        with ProcessPoolExecutor(max_workers=4) as exe:
            exe.submit(thread_240p, video_file)
            exe.submit(thread_480p, video_file)
            exe.submit(thread_720p, video_file)
            exe.submit(thread_1080p, video_file)
        master = Masterm3u8.master_1080p(file_name)
        convert_480p_mp4(video_file, path_dir)

    hls_file = os.path.join(path_dir, f'{file_name}.m3u8')
    hls_file_path = os.path.relpath(hls_file, os.path.abspath(start_dir))
    file_mp4 = os.path.join(path_dir, f'{file_name}.mp4')
    path_mp4 = os.path.relpath(file_mp4, os.path.abspath(start_dir))
    f = open(hls_file, 'w')
    f.write(master)
    f.close()
    return {'hls_file_path': hls_file_path, 'path_mp4': path_mp4 }
