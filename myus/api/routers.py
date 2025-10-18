from ninja import NinjaAPI
from api.apis.auth import AuthAPI
from api.apis.user import UserAPI
from api.apis.media import VideoAPI, MusicAPI, ComicAPI, PictureAPI, BlogAPI, ChatAPI

api = NinjaAPI(title="MyUs API")

# Auth
api.add_router("/auth", AuthAPI().router, tags=["auth"])

# User
api.add_router("/user", UserAPI().router, tags=["user"])

# # Setting
# api.add_router("/setting/profile", setting_profile_router)
# api.add_router("/setting/mypage", setting_mypage_router)
# api.add_router("/setting/notification", setting_notification_router)

# # Media
# api.add_router("/home", HomeAPI().router, tags=["Media Home"])
api.add_router("/media/video", VideoAPI().router, tags=["Media Video"])
api.add_router("/media/music", MusicAPI().router, tags=["Media Music"])
api.add_router("/media/comic", ComicAPI().router, tags=["Media Comic"])
api.add_router("/media/picture", PictureAPI().router, tags=["Media Picture"])
api.add_router("/media/blog", BlogAPI().router, tags=["Media Blog"])
api.add_router("/media/chat", ChatAPI().router, tags=["Media Chat"])
# api.add_router("/media/comment", CommentAPI().router, tags=["Media Comment"])
