from api.db.models.media import Video, Music, Blog, Comic, Picture, Chat


type MediaModel = Video | Music | Blog | Comic | Picture | Chat


media_models: dict[str, type[MediaModel]] = {
    'Video': Video,
    'Music': Music,
    'Blog': Blog,
    'Comic': Comic,
    'Picture': Picture,
    'Chat': Chat,
}

model_media_comment_dict = {
    "video"  : Video,
    "music"  : Music,
    "blog"   : Blog,
    "comic"  : Comic,
    "picture": Picture,
}
