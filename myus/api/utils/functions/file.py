def user_image(instance, filename):
    class_name = type(instance).__name__.lower()
    return f"images/{class_name}/user_{instance.id}/{filename}"


def image_upload(instance, filename):
    class_name = type(instance).__name__.lower()
    return f"images/{class_name}/user_{instance.author_id}/object_{instance.id}/{filename}"


def video_upload(instance, filename):
    class_name = type(instance).__name__.lower()
    return f"videos/{class_name}/user_{instance.author_id}/object_{instance.id}/{filename}"


def musics_upload(instance, filename):
    return f"musics/user_{instance.author_id}/object_{instance.id}/{filename}"


def comic_upload(instance, filename):
    comic = instance.comic
    return f"comics/user_{comic.author_id}/object_{comic.id}/{filename}"
