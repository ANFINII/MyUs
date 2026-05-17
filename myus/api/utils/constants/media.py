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

model_list = [Video, Music, Blog, Comic, Picture, Chat]

model_dict = {
    Video  : "video",
    Music  : "music",
    Blog   : "blog",
    Comic  : "comic",
    Picture: "picture",
    Chat   : "chat",
}

model_pjax = {
    "media/video"  : Video,
    "media/music"  : Music,
    "media/blog"   : Blog,
    "media/comic"  : Comic,
    "media/picture": Picture,
    "media/chat"   : Chat,
}

model_create_pjax = (
    "media/video/create",
    "media/music/create",
    "media/blog/create",
    "media/comic/create",
    "media/picture/create",
    "media/chat/create",
)

model_like_dict = {
    "video/detail"  : Video,
    "music/detail"  : Music,
    "blog/detail"   : Blog,
    "comic/detail"  : Comic,
    "picture/detail": Picture,
    "chat/detail"   : Chat,
}

model_media_comment_dict = {
    "video"  : Video,
    "music"  : Music,
    "blog"   : Blog,
    "comic"  : Comic,
    "picture": Picture,
}

model_media_comment_no_dict = {
    "video"  : 1,
    "music"  : 2,
    "blog"   : 3,
    "comic"  : 4,
    "picture": 5,
}

model_comment_dict = {
    "video/detail"  : Video,
    "music/detail"  : Music,
    "blog/detail"   : Blog,
    "comic/detail"  : Comic,
    "picture/detail": Picture,
}
