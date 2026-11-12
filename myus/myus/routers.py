from ninja import NinjaAPI
from myus.adapter.advertise import AdvertiseAPI
from myus.adapter.auth import AuthAPI
from myus.adapter.category import CategoryAPI
from myus.adapter.comment import CommentAPI
from myus.adapter.hashtag import MediaHashtagAPI
from myus.adapter.manage import ManageVideoAPI, ManageMusicAPI, ManageBlogAPI, ManageComicAPI, ManagePictureAPI, ManageChatAPI, ManageAdvertiseAPI
from myus.adapter.media import HomeAPI, RecommendAPI, VideoAPI, MusicAPI, BlogAPI, ComicAPI, PictureAPI, ChatAPI, MediaReadAPI
from myus.adapter.message import MessageAPI
from myus.adapter.channel import ChannelAPI
from myus.adapter.payment import PaymentAPI
from myus.adapter.setting import SettingMyPageAPI, SettingNotificationAPI, SettingProfileAPI
from myus.adapter.user import UserAPI


api = NinjaAPI(title="MyUs API")

api.add_router("/auth", AuthAPI().router, tags=["auth"])
api.add_router("/user", UserAPI().router, tags=["user"])

api.add_router("/setting/profile", SettingProfileAPI().router, tags=["Setting"])
api.add_router("/setting/mypage", SettingMyPageAPI().router, tags=["Setting"])
api.add_router("/setting/notification", SettingNotificationAPI().router, tags=["Setting"])
api.add_router("/payment", PaymentAPI().router, tags=["Payment"])

api.add_router("/manage/media/video", ManageVideoAPI().router, tags=["Manage Video"])
api.add_router("/manage/media/music", ManageMusicAPI().router, tags=["Manage Music"])
api.add_router("/manage/media/blog", ManageBlogAPI().router, tags=["Manage Blog"])
api.add_router("/manage/media/comic", ManageComicAPI().router, tags=["Manage Comic"])
api.add_router("/manage/media/picture", ManagePictureAPI().router, tags=["Manage Picture"])
api.add_router("/manage/media/chat", ManageChatAPI().router, tags=["Manage Chat"])
api.add_router("/manage/advertise", ManageAdvertiseAPI().router, tags=["Manage Advertise"])

api.add_router("/channel", ChannelAPI().router, tags=["Channel"])
api.add_router("/media/home", HomeAPI().router, tags=["Media Home"])
api.add_router("/media/recommend", RecommendAPI().router, tags=["Media Recommend"])
api.add_router("/media/video", VideoAPI().router, tags=["Media Video"])
api.add_router("/media/music", MusicAPI().router, tags=["Media Music"])
api.add_router("/media/blog", BlogAPI().router, tags=["Media Blog"])
api.add_router("/media/comic", ComicAPI().router, tags=["Media Comic"])
api.add_router("/media/picture", PictureAPI().router, tags=["Media Picture"])
api.add_router("/media/chat", ChatAPI().router, tags=["Media Chat"])
api.add_router("/media/read", MediaReadAPI().router, tags=["Media Read"])

api.add_router("/media/category", CategoryAPI().router, tags=["Media Category"])
api.add_router("/media/hashtag", MediaHashtagAPI().router, tags=["Media Hashtag"])
api.add_router("/media/comment", CommentAPI().router, tags=["Media Comment"])
api.add_router("/media/message", MessageAPI().router, tags=["Media Message"])

api.add_router("/advertise", AdvertiseAPI().router, tags=["Advertise"])
