from api.utils.enum.index import ImageType, VideoType
from api.utils.functions.index import new_ulid
from api.db.models.channel import Channel
from api.db.models.media import Video, Music, Comic, Picture, Blog
from api.db.models.user import User, MyPage


def avatar_path(type: ImageType, ulid: str, filename: str) -> str:
    return f"images/{type}/{ulid}/{new_ulid()}_{filename}"


def image_path(type: ImageType, ulid: str, filename: str) -> str:
    return f"images/{type}/channel_{ulid}/{new_ulid()}_{filename}"


def video_path(type: VideoType, ulid: str, filename: str) -> str:
    return f"videos/{type}/channel_{ulid}/{new_ulid()}_{filename}"


def musics_path(ulid: str, filename: str) -> str:
    return f"musics/channel_{ulid}/{new_ulid()}_{filename}"


def comic_path(ulid: str, filename: str) -> str:
    return f"comics/channel_{ulid}/{new_ulid()}_{filename}"


def avatar_upload(obj: User | MyPage | Channel, ulid: str, filename: str) -> str:
    type_map: dict[str, ImageType] = {
        "User": ImageType.USER,
        "MyPage": ImageType.USER,
        "Channel": ImageType.CHANNEL,
    }
    image_type = type_map[type(obj).__name__]
    return avatar_path(image_type, ulid, filename)


def image_upload(obj: Video | Comic | Picture | Blog, filename: str) -> str:
    type_map: dict[str, ImageType] = {
        "Video": ImageType.VIDEO,
        "Comic": ImageType.COMIC,
        "Picture": ImageType.PICTURE,
        "Blog": ImageType.BLOG,
    }
    image_type = type_map[type(obj).__name__]
    return image_path(image_type, str(obj.channel.ulid), filename)


def video_upload(obj: Video, filename: str) -> str:
    return video_path(VideoType.VIDEO, str(obj.channel.ulid), filename)


def music_upload(obj: Music, filename: str) -> str:
    return musics_path(str(obj.channel.ulid), filename)


def comic_upload(obj: Comic, filename: str) -> str:
    return comic_path(str(obj.channel.ulid), filename)
