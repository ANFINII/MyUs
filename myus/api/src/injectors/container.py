from injector import Injector, Module
from api.src.injectors.index import (
    UserModule,
    ChannelModule,
    MediaModule,
    CommentModule,
    MessageModule,
    HashtagModule,
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
    CommentModule(),
    MessageModule(),
    HashtagModule(),
    SearchTagModule(),
    NotificationModule(),
    FollowModule(),
    SubscribeModule(),
    NgWordModule(),
]

injector = Injector(modules)
