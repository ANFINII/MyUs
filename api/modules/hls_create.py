import os
import sys
import subprocess
import codecs
import requests

# videos/videos_video/{instance.author.id}/{instance.id}/video_360p.mp4
# videos/videos_video/{instance.author.id}/{instance.id}/video_list.m3u8
# videos/videos_video/{instance.author.id}/{instance.id}/1080p/video_1080p.m3u8
# videos/videos_video/{instance.author.id}/{instance.id}/720p/video_720p.m3u8
# videos/videos_video/{instance.author.id}/{instance.id}/480p/video_480p.m3u8
# videos/videos_video/{instance.author.id}/{instance.id}/360p/video_360p.m3u8
# videos/videos_video/{instance.author.id}/{instance.id}/240p/video_240p.m3u8

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
VIDEOS_PATH = os.path.join(MEDIA_ROOT, 'videos')
ABSOLUTE_PATH = os.path.abspath(VIDEOS_PATH)

def create_mp4(mp4, path_dir, start):
    # mp4の作成 (input.mp4 -> video_360p.mp4)
    path_360p = os.path.join(path_dir, 'video_360p.mp4')
    path_360p1 = os.path.relpath(path_360p, os.path.abspath(start))
    print(start)
    print(path_360p1)
    c = 'ffmpeg'
    c += ' -i ' + mp4
    c += ' -f mp4 -vcodec h264 -vb 500k -s 640x360 -pix_fmt yuv420p'
    c += ' -ac 2 -ar 48000 -ab 128k -acodec aac -strict experimental'
    c += ' -movflags faststart'
    c += ' video_360p.mp4'
    code = subprocess.call(c.split(), shell=True)
    print('process=' + str(code))
    f = codecs.open(path_360p, 'w', 'utf-8')
    f.write(c)
    f.close()
    return path_360p1

def create_hls(mp4, path_dir, start):
    # m3u8の作成 (input.mp4 -> 1080p/video_1080p.m3u8)
    # path_1080p = os.path.join(path_dir, '1080p', 'video_1080p.m3u8')
    # path_1080p_s = os.path.relpath(path_1080p, VIDEOS_PATH)
    c = 'ffmpeg'
    c += ' -i ' + mp4
    c += ' -codec copy -vbsf h264_mp4toannexb -map 0'
    c += ' -f segment -segment_format mpegts -segment_time 10'
    c += ' -segment_list 1080p/video_1080p.m3u8'
    c += ' 1080p/video_1080p_%5d.ts'
    code = subprocess.call(c.split(), shell=True)
    # f = codecs.open(path_1080p, 'w', 'utf-8')
    # f.write(c)
    # f.close()
    print('process=' + str(code))

    # m3u8の作成 (input.mp4 -> 720p/video_720p.m3u8)
    c = 'ffmpeg'
    c += ' -i ' + mp4
    c += ' -codec copy -vbsf h264_mp4toannexb -map 0'
    c += ' -f segment -segment_format mpegts -segment_time 10'
    c += ' -segment_list 720p/video_720p.m3u8'
    c += ' 720p/video_720p_%5d.ts'
    code = subprocess.call(c.split(), shell=True)
    print('process=' + str(code))

    # m3u8の作成 (input.mp4 -> 480p/video_480p.m3u8)
    c = 'ffmpeg'
    c += ' -i ' + mp4
    c += ' -codec copy -vbsf h264_mp4toannexb -map 0'
    c += ' -f segment -segment_format mpegts -segment_time 10'
    c += ' -segment_list 480p/video_480p.m3u8'
    c += ' 480p/video_480p_%5d.ts'
    code = subprocess.call(c.split(), shell=True)
    print('process=' + str(code))

    # m3u8の作成 (input.mp4 -> 360p/video_360p.m3u8)
    c = 'ffmpeg'
    c += ' -i ' + mp4
    c += ' -codec copy -vbsf h264_mp4toannexb -map 0'
    c += ' -f segment -segment_format mpegts -segment_time 10'
    c += ' -segment_list 360p/video_360p.m3u8'
    c += ' 360p/video_360p_%5d.ts'
    code = subprocess.call(c.split(), shell=True)
    print('process=' + str(code))

    # m3u8の作成 (input.mp4 -> 240p/video_240p.m3u8)
    c = 'ffmpeg'
    c += ' -i ' + mp4
    c += ' -codec copy -vbsf h264_mp4toannexb -map 0'
    c += ' -f segment -segment_format mpegts -segment_time 10'
    c += ' -segment_list 240p/video_240p.m3u8'
    c += ' 240p/video_240p_%5d.ts'
    code = subprocess.call(c.split(), shell=True)
    print('process=' + str(code))


    # マスタm3u8の作成 (->video_list.m3u8)
    path_video_list = os.path.join(path_dir, 'video_list.m3u8')
    path_video_list1 = os.path.relpath(path_video_list, os.path.abspath(start))
    print(path_video_list1)
    t = '#EXTM3U'
    t += '\n##EXT-X-VERSION:3'
    t += '\n#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=4000000,RESOLUTION=1920x1080'
    t += '\n1080p/video_1080p.m3u8'
    t += '\n#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1800000,RESOLUTION=1280x720'
    t += '\n720p/video_720p.m3u8'
    t += '\n#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=800000,RESOLUTION=854x480'
    t += '\n480p/video_480p.m3u8'
    t += '\n#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=450000,RESOLUTION=640x360'
    t += '\n360p/video_360p.m3u8'
    t += '\n#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=200000,RESOLUTION=426x240'
    t += '\n240p/video_240p.m3u8'
    f = codecs.open(path_video_list, 'w', 'utf-8')
    f.write(t)
    f.close()
    return path_video_list1

if __name__ == "__main__":
    create_hls()
