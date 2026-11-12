from injector import Injector, Module
from myus.injectors.index import (
    UserModule,
    ChannelModule,
    MediaModule,
    AdvertiseModule,
    CategoryModule,
    HashtagModule,
    CommentModule,
    MessageModule,
    SearchTagModule,
    NotificationModule,
    AccessLogModule,
    FollowModule,
    SubscribeModule,
    NgWordModule,
    PaymentModule,
    EsModule,
)


modules: list[Module] = [
    UserModule(),
    ChannelModule(),
    MediaModule(),
    AdvertiseModule(),
    CategoryModule(),
    HashtagModule(),
    CommentModule(),
    MessageModule(),
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
