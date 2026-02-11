from injector import Injector, Module
from api.src.injectors.index import (
    UserModule,
    ChannelModule,
    MediaModule,
    CommentModule,
    MessageModule,
    FollowModule,
    SearchTagModule,
    NotificationModule,
)


modules: list[Module] = [
    UserModule(),
    ChannelModule(),
    MediaModule(),
    CommentModule(),
    MessageModule(),
    FollowModule(),
    SearchTagModule(),
    NotificationModule(),
]

injector = Injector(modules)
