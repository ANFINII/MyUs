from injector import Injector, Module
from api.src.injectors.index import (
    UserModule,
    AuthModule,
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
)


modules: list[Module] = [
    UserModule(),
    AuthModule(),
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
]

injector = Injector(modules)
