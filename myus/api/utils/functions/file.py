def user_image(instance, filename):
    class_name = type(instance).__name__.lower()
    return f"images/{class_name}/user_{instance.id}/{filename}"


def channel_image(instance, filename):
    return f"images/channel/channel_{instance.id}/{filename}"


def image_upload(instance, filename):
    class_name = type(instance).__name__.lower()
    return f"images/{class_name}/channel_{instance.channel_id}/object_{instance.id}/{filename}"


def video_upload(instance, filename):
    class_name = type(instance).__name__.lower()
    return f"videos/{class_name}/channel_{instance.channel_id}/object_{instance.id}/{filename}"


def musics_upload(instance, filename):
    return f"musics/channel_{instance.channel_id}/object_{instance.id}/{filename}"


def comic_upload(instance, filename):
    comic = instance.comic
    return f"comics/channel_{comic.channel_id}/object_{comic.id}/{filename}"
