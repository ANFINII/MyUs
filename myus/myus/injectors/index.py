from injector import Module, multiprovider, provider, singleton
from myus.adapter.outbound.payment.stripe.provider import StripeProvider
from myus.domain.aggregate.subscription.event import SUBSCRIPTION_EVENT_CLASSES
from myus.adapter.outbound.db.payment.customer.repository import PaymentCustomerRepository
from myus.adapter.outbound.db.payment.event.repository import PaymentEventRepository
from myus.adapter.outbound.db.payment.ledger.repository import LedgerEntryRepository
from myus.adapter.outbound.db.payment.payout.repository import PayoutRepository
from myus.adapter.outbound.db.payment.subscription.repository import SubscriptionRepository
from myus.adapter.outbound.db.payment.transaction.repository import TransactionRepository
from myus.adapter.outbound.db.user.repository import UserRepository
from myus.adapter.outbound.db.category.repository import CategoryRepository
from myus.adapter.outbound.db.channel.repository import ChannelRepository
from myus.adapter.outbound.db.media.video.repository import VideoRepository
from myus.adapter.outbound.db.media.music.repository import MusicRepository
from myus.adapter.outbound.db.media.blog.repository import BlogRepository
from myus.adapter.outbound.db.media.comic.repository import ComicRepository
from myus.adapter.outbound.db.media.picture.repository import PictureRepository
from myus.adapter.outbound.db.media.chat.repository import ChatRepository
from myus.adapter.outbound.db.advertise.repository import AdvertiseRepository
from myus.adapter.outbound.db.comment.repository import CommentRepository
from myus.adapter.outbound.db.message.repository import MessageRepository
from myus.adapter.outbound.db.follow.repository import FollowRepository
from myus.adapter.outbound.db.subscribe.repository import SubscribeRepository
from myus.adapter.outbound.db.hashtag.repository import HashtagRepository
from myus.adapter.outbound.db.ng_word.repository import NgWordRepository
from myus.adapter.outbound.db.search_tag.repository import SearchTagRepository
from myus.adapter.outbound.db.notification.repository import NotificationRepository
from myus.adapter.outbound.db.access_log.repository import AccessLogRepository
from myus.adapter.outbound.db.es.repository import EventStoreRepository
from myus.domain.interface.user.interface import UserInterface
from myus.domain.interface.category.interface import CategoryInterface
from myus.domain.interface.channel.interface import ChannelInterface
from myus.domain.interface.media.video.interface import VideoInterface
from myus.domain.interface.media.music.interface import MusicInterface
from myus.domain.interface.media.blog.interface import BlogInterface
from myus.domain.interface.media.comic.interface import ComicInterface
from myus.domain.interface.media.picture.interface import PictureInterface
from myus.domain.interface.media.chat.interface import ChatInterface
from myus.domain.interface.advertise.interface import AdvertiseInterface
from myus.domain.interface.comment.interface import CommentInterface
from myus.domain.interface.message.interface import MessageInterface
from myus.domain.interface.follow.interface import FollowInterface
from myus.domain.interface.subscribe.interface import SubscribeInterface
from myus.domain.interface.hashtag.interface import HashtagInterface
from myus.domain.interface.ng_word.interface import NgWordInterface
from myus.domain.interface.search_tag.interface import SearchTagInterface
from myus.domain.interface.notification.interface import NotificationInterface
from myus.domain.interface.access_log.interface import AccessLogInterface
from myus.domain.interface.payment.customer.interface import PaymentCustomerInterface
from myus.domain.interface.payment.event.interface import PaymentEventInterface
from myus.domain.interface.payment.ledger.interface import LedgerEntryInterface
from myus.domain.interface.payment.payout.interface import PayoutInterface
from myus.domain.interface.payment.provider.interface import PaymentInterface
from myus.domain.interface.payment.subscription.interface import SubscriptionInterface
from myus.domain.interface.payment.transaction.interface import TransactionInterface
from myus.domain.interface.es.interface import EventStoreInterface
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
