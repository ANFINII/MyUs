class Masterm3u8:
    def master_360p(file_name):
        master = (
            "#EXTM3U\n"
            "#EXT-X-VERSION:3\n"
            "#EXT-X-STREAM-INF:BANDWIDTH=162816,RESOLUTION=256x144,NAME='144'\n"
            f"{file_name}_144p.m3u8\n"
            "#EXT-X-STREAM-INF:BANDWIDTH=413696,RESOLUTION=640x360,NAME='360'\n"
            f"{file_name}_360p.m3u8\n"
        )
        return master

    def master_480p(file_name):
        master = (
            "#EXTM3U\n"
            "#EXT-X-VERSION:3\n"
            "#EXT-X-STREAM-INF:BANDWIDTH=249856,RESOLUTION=426x240,NAME='240'\n"
            f"{file_name}_240p.m3u8\n"
            "#EXT-X-STREAM-INF:BANDWIDTH=964608,RESOLUTION=854x480,NAME='480'\n"
            f"{file_name}_480p.m3u8\n"
        )
        return master

    def master_720p(file_name):
        master = (
            "#EXTM3U\n"
            "#EXT-X-VERSION:3\n"
            "#EXT-X-STREAM-INF:BANDWIDTH=249856,RESOLUTION=426x240,NAME='240'\n"
            f"{file_name}_240p.m3u8\n"
            "#EXT-X-STREAM-INF:BANDWIDTH=964608,RESOLUTION=854x480,NAME='480'\n"
            f"{file_name}_480p.m3u8\n"
            "#EXT-X-STREAM-INF:BANDWIDTH=2424832,RESOLUTION=1280x720,NAME='720'\n"
            f"{file_name}_720p.m3u8\n"
        )
        return master

    def master_1080p(file_name):
        master = (
            "#EXTM3U\n"
            "#EXT-X-VERSION:3\n"
            "#EXT-X-STREAM-INF:BANDWIDTH=249856,RESOLUTION=426x240,NAME='240'\n"
            f"{file_name}_240p.m3u8\n"
            "#EXT-X-STREAM-INF:BANDWIDTH=964608,RESOLUTION=854x480,NAME='480'\n"
            f"{file_name}_480p.m3u8\n"
            "#EXT-X-STREAM-INF:BANDWIDTH=2424832,RESOLUTION=1280x720,NAME='720'\n"
            f"{file_name}_720p.m3u8\n"
            "#EXT-X-STREAM-INF:BANDWIDTH=4521984,RESOLUTION=1920x1080,NAME='1080'\n"
            f"{file_name}_1080p.m3u8\n"
        )
        return master
