from api.db.models.media import Video, Music, Blog, Comic, Picture


model_media_comment_dict: dict[str, type[Video] | type[Music] | type[Blog] | type[Comic] | type[Picture]] = {
    "video"  : Video,
    "music"  : Music,
    "blog"   : Blog,
    "comic"  : Comic,
    "picture": Picture,
}
