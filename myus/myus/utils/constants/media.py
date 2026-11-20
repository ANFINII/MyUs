from myus.db.models.media import Video, Audio, Blog, Comic, Picture


model_media_comment_dict: dict[str, type[Video] | type[Audio] | type[Blog] | type[Comic] | type[Picture]] = {
    "video"  : Video,
    "audio"  : Audio,
    "blog"   : Blog,
    "comic"  : Comic,
    "picture": Picture,
}
