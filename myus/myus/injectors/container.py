from injector import Injector
from .module import (
    UserModule,
    ChannelModule,
    MediaModule,
    AdvertiseModule,
    CategoryModule,
    HashtagModule,
    CommentModule,
    MessageModule,
    PlaylistModule,
    SeriesModule,
    SearchTagModule,
    NotificationModule,
    AccessLogModule,
    FollowModule,
    SubscribeModule,
    NgWordModule,
    PaymentModule,
    EsModule,
)


modules = [
    UserModule(),
    ChannelModule(),
    MediaModule(),
    AdvertiseModule(),
    CategoryModule(),
    HashtagModule(),
    CommentModule(),
    MessageModule(),
    PlaylistModule(),
    SeriesModule(),
    SearchTagModule(),
    NotificationModule(),
    AccessLogModule(),
    FollowModule(),
    SubscribeModule(),
    NgWordModule(),
    PaymentModule(),
    EsModule(),
]

injector = Injector(modules)
