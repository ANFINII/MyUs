from api.utils.functions.index import new_ulid


def avatar_image(type: str, ulid: str, filename: str):
    return f"images/{type}/{ulid}/{new_ulid()}_{filename}"


def image_upload(type: str, ulid: str, filename: str):
    return f"images/{type}/channel_{ulid}/{new_ulid()}_{filename}"


def video_upload(type: str, ulid: str, filename: str):
    return f"videos/{type}/channel_{ulid}/{new_ulid()}_{filename}"


def musics_upload(ulid: str, filename: str):
    return f"musics/channel_{ulid}/{new_ulid()}_{filename}"


def comic_upload(ulid: str, filename: str):
    return f"comics/channel_{ulid}/{new_ulid()}_{filename}"
