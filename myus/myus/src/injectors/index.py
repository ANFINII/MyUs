from injector import Module, multiprovider, provider, singleton
from myus.src.adapter.external.payment.stripe.provider import StripeProvider
from myus.src.domain.aggregate.subscription.event import SUBSCRIPTION_EVENT_CLASSES
from myus.src.domain.entity.payment.customer.repository import PaymentCustomerRepository
from myus.src.domain.entity.payment.event.repository import PaymentEventRepository
from myus.src.domain.entity.payment.ledger.repository import LedgerEntryRepository
from myus.src.domain.entity.payment.payout.repository import PayoutRepository
from myus.src.domain.entity.payment.subscription.repository import SubscriptionRepository
from myus.src.domain.entity.payment.transaction.repository import TransactionRepository
from myus.src.domain.entity.user.repository import UserRepository
from myus.src.domain.entity.category.repository import CategoryRepository
from myus.src.domain.entity.channel.repository import ChannelRepository
from myus.src.domain.entity.media.video.repository import VideoRepository
from myus.src.domain.entity.media.music.repository import MusicRepository
from myus.src.domain.entity.media.blog.repository import BlogRepository
from myus.src.domain.entity.media.comic.repository import ComicRepository
from myus.src.domain.entity.media.picture.repository import PictureRepository
from myus.src.domain.entity.media.chat.repository import ChatRepository
from myus.src.domain.entity.advertise.repository import AdvertiseRepository
from myus.src.domain.entity.comment.repository import CommentRepository
from myus.src.domain.entity.message.repository import MessageRepository
from myus.src.domain.entity.follow.repository import FollowRepository
from myus.src.domain.entity.subscribe.repository import SubscribeRepository
from myus.src.domain.entity.hashtag.repository import HashtagRepository
from myus.src.domain.entity.ng_word.repository import NgWordRepository
from myus.src.domain.entity.search_tag.repository import SearchTagRepository
from myus.src.domain.entity.notification.repository import NotificationRepository
from myus.src.domain.entity.access_log.repository import AccessLogRepository
from myus.src.domain.entity.es.repository import EventStoreRepository
from myus.src.domain.interface.user.interface import UserInterface
from myus.src.domain.interface.category.interface import CategoryInterface
from myus.src.domain.interface.channel.interface import ChannelInterface
from myus.src.domain.interface.media.video.interface import VideoInterface
from myus.src.domain.interface.media.music.interface import MusicInterface
from myus.src.domain.interface.media.blog.interface import BlogInterface
from myus.src.domain.interface.media.comic.interface import ComicInterface
from myus.src.domain.interface.media.picture.interface import PictureInterface
from myus.src.domain.interface.media.chat.interface import ChatInterface
from myus.src.domain.interface.advertise.interface import AdvertiseInterface
from myus.src.domain.interface.comment.interface import CommentInterface
from myus.src.domain.interface.message.interface import MessageInterface
from myus.src.domain.interface.follow.interface import FollowInterface
from myus.src.domain.interface.subscribe.interface import SubscribeInterface
from myus.src.domain.interface.hashtag.interface import HashtagInterface
from myus.src.domain.interface.ng_word.interface import NgWordInterface
from myus.src.domain.interface.search_tag.interface import SearchTagInterface
from myus.src.domain.interface.notification.interface import NotificationInterface
from myus.src.domain.interface.access_log.interface import AccessLogInterface
from myus.src.domain.interface.payment.customer.interface import PaymentCustomerInterface
from myus.src.domain.interface.payment.event.interface import PaymentEventInterface
from myus.src.domain.interface.payment.ledger.interface import LedgerEntryInterface
from myus.src.domain.interface.payment.payout.interface import PayoutInterface
from myus.src.domain.interface.payment.provider.interface import PaymentInterface
from myus.src.domain.interface.payment.subscription.interface import SubscriptionInterface
from myus.src.domain.interface.payment.transaction.interface import TransactionInterface
from myus.src.domain.interface.es.interface import EventStoreInterface
from myus.utils.enum.payment import PaymentProvider


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
    def provide_blog_repository(self) -> BlogInterface:
        return BlogRepository()

    @provider
    def provide_comic_repository(self) -> ComicInterface:
        return ComicRepository()

    @provider
    def provide_picture_repository(self) -> PictureInterface:
        return PictureRepository()

    @provider
    def provide_chat_repository(self) -> ChatInterface:
        return ChatRepository()


class CategoryModule(Module):
    @provider
    def provide_category_repository(self) -> CategoryInterface:
        return CategoryRepository()


class HashtagModule(Module):
    @provider
    def provide_hashtag_repository(self) -> HashtagInterface:
        return HashtagRepository()


class CommentModule(Module):
    @provider
    def provide_comment_repository(self) -> CommentInterface:
        return CommentRepository()


class MessageModule(Module):
    @provider
    def provide_message_repository(self) -> MessageInterface:
        return MessageRepository()


class NgWordModule(Module):
    @provider
    def provide_ng_word_repository(self) -> NgWordInterface:
        return NgWordRepository()


class SearchTagModule(Module):
    @provider
    def provide_search_tag_repository(self) -> SearchTagInterface:
        return SearchTagRepository()


class NotificationModule(Module):
    @provider
    def provide_notification_repository(self) -> NotificationInterface:
        return NotificationRepository()


class AccessLogModule(Module):
    @provider
    def provide_access_log_repository(self) -> AccessLogInterface:
        return AccessLogRepository()


class FollowModule(Module):
    @provider
    def provide_follow_repository(self) -> FollowInterface:
        return FollowRepository()


class SubscribeModule(Module):
    @provider
    def provide_subscribe_repository(self) -> SubscribeInterface:
        return SubscribeRepository()


class AdvertiseModule(Module):
    @provider
    def provide_advertise_repository(self) -> AdvertiseInterface:
        return AdvertiseRepository()


class PaymentModule(Module):
    @singleton
    @multiprovider
    def provide_payment_providers(self) -> dict[PaymentProvider, PaymentInterface]:
        return {PaymentProvider.STRIPE: StripeProvider()}

    @provider
    def provide_payment_event_repository(self) -> PaymentEventInterface:
        return PaymentEventRepository()

    @provider
    def provide_payment_customer_repository(self) -> PaymentCustomerInterface:
        return PaymentCustomerRepository()

    @provider
    def provide_subscription_repository(self) -> SubscriptionInterface:
        return SubscriptionRepository()

    @provider
    def provide_transaction_repository(self) -> TransactionInterface:
        return TransactionRepository()

    @provider
    def provide_ledger_entry_repository(self) -> LedgerEntryInterface:
        return LedgerEntryRepository()

    @provider
    def provide_payout_repository(self) -> PayoutInterface:
        return PayoutRepository()


class EsModule(Module):
    @provider
    def provide_event_store_repository(self) -> EventStoreInterface:
        return EventStoreRepository(SUBSCRIPTION_EVENT_CLASSES)
