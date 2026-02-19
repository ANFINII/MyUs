from injector import Injector, Module
from api.src.injectors.index import (
    UserModule,
    ChannelModule,
    MediaModule,
    CommentModule,
    MessageModule,
    SearchTagModule,
    NotificationModule,
    FollowModule,
    SubscribeModule,
)


modules: list[Module] = [
    UserModule(),
    ChannelModule(),
    MediaModule(),
    CommentModule(),
    MessageModule(),
    SearchTagModule(),
    NotificationModule(),
    FollowModule(),
    SubscribeModule(),
]

injector = Injector(modules)
