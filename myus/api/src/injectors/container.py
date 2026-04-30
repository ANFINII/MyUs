from injector import Injector, Module
from api.src.injectors.index import (
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
    FollowModule,
    SubscribeModule,
    NgWordModule,
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
    FollowModule(),
    SubscribeModule(),
    NgWordModule(),
]

injector = Injector(modules)
