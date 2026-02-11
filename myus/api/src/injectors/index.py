from injector import Module, provider
from api.src.domain.entity.user.repository import UserRepository
from api.src.domain.entity.channel.repository import ChannelRepository
from api.src.domain.entity.media.video.repository import VideoRepository
from api.src.domain.entity.media.music.repository import MusicRepository
from api.src.domain.entity.media.picture.repository import PictureRepository
from api.src.domain.entity.media.blog.repository import BlogRepository
from api.src.domain.entity.media.comic.repository import ComicRepository
from api.src.domain.entity.media.chat.repository import ChatRepository
from api.src.domain.entity.comment.repository import CommentRepository
from api.src.domain.entity.message.repository import MessageRepository
from api.src.domain.entity.follow.repository import FollowRepository
from api.src.domain.entity.search_tag.repository import SearchTagRepository
from api.src.domain.entity.notification.repository import NotificationRepository
from api.src.domain.interface.user.interface import UserInterface
from api.src.domain.interface.channel.interface import ChannelInterface
from api.src.domain.interface.media.video.interface import VideoInterface
from api.src.domain.interface.media.music.interface import MusicInterface
from api.src.domain.interface.media.picture.interface import PictureInterface
from api.src.domain.interface.media.blog.interface import BlogInterface
from api.src.domain.interface.media.comic.interface import ComicInterface
from api.src.domain.interface.media.chat.interface import ChatInterface
from api.src.domain.interface.comment.interface import CommentInterface
from api.src.domain.interface.message.interface import MessageInterface
from api.src.domain.interface.follow.interface import FollowInterface
from api.src.domain.interface.search_tag.interface import SearchTagInterface
from api.src.domain.interface.notification.interface import NotificationInterface


class UserModule(Module):
    @provider
    def provide_user_repository(self) -> UserInterface:
        return UserRepository()


class ChannelModule(Module):
    @provider
    def provide_channel_repository(self) -> ChannelInterface:
        return ChannelRepository()


class MediaModule(Module):
    @provider
    def provide_video_repository(self) -> VideoInterface:
        return VideoRepository()

    @provider
    def provide_music_repository(self) -> MusicInterface:
        return MusicRepository()

    @provider
    def provide_comic_repository(self) -> ComicInterface:
        return ComicRepository()

    @provider
    def provide_picture_repository(self) -> PictureInterface:
        return PictureRepository()

    @provider
    def provide_blog_repository(self) -> BlogInterface:
        return BlogRepository()

    @provider
    def provide_chat_repository(self) -> ChatInterface:
        return ChatRepository()


class CommentModule(Module):
    @provider
    def provide_comment_repository(self) -> CommentInterface:
        return CommentRepository()


class MessageModule(Module):
    @provider
    def provide_message_repository(self) -> MessageInterface:
        return MessageRepository()


class FollowModule(Module):
    @provider
    def provide_follow_repository(self) -> FollowInterface:
        return FollowRepository()


class SearchTagModule(Module):
    @provider
    def provide_search_tag_repository(self) -> SearchTagInterface:
        return SearchTagRepository()


class NotificationModule(Module):
    @provider
    def provide_notification_repository(self) -> NotificationInterface:
        return NotificationRepository()
