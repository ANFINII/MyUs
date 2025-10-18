"""ユーザー関連のAPI"""

from ninja import Router
from api.modules.logger import log


class UserAPI:
    """ユーザーAPI"""

    def __init__(self) -> None:
        self.me_router = Router(tags=["user"])
        self.search_tag_router = Router(tags=["user"])
        self.follow_router = Router(tags=["user"])
        self.follower_router = Router(tags=["user"])
        self.like_media_router = Router(tags=["user"])
        self.like_comment_router = Router(tags=["user"])
        self.notification_router = Router(tags=["user"])
        self._register_routes()

    def _register_routes(self) -> None:
        """ルートを登録"""

        @self.me_router.get("")
        def get_current_user(request) -> dict[str, str]:
            """現在のユーザー情報を取得"""
            log.info("Get current user")
            return {"message": "Get current user endpoint (to be implemented)"}

        @self.search_tag_router.get("")
        def search_tag(request, query: str) -> dict[str, str]:
            """タグ検索"""
            log.info("Search tag", query=query)
            return {"message": "Search tag endpoint (to be implemented)", "query": query}

        @self.follow_router.get("")
        @self.follow_router.post("")
        def follow(request) -> dict[str, str]:
            """フォロー一覧取得/フォロー実行"""
            log.info("Follow endpoint")
            return {"message": "Follow endpoint (to be implemented)"}

        @self.follower_router.get("")
        def follower(request) -> dict[str, str]:
            """フォロワー一覧取得"""
            log.info("Follower endpoint")
            return {"message": "Follower endpoint (to be implemented)"}

        @self.like_media_router.get("")
        @self.like_media_router.post("")
        def like_media(request) -> dict[str, str]:
            """メディアいいね一覧取得/いいね実行"""
            log.info("Like media endpoint")
            return {"message": "Like media endpoint (to be implemented)"}

        @self.like_comment_router.get("")
        @self.like_comment_router.post("")
        def like_comment(request) -> dict[str, str]:
            """コメントいいね一覧取得/いいね実行"""
            log.info("Like comment endpoint")
            return {"message": "Like comment endpoint (to be implemented)"}

        @self.notification_router.get("")
        def notification(request) -> dict[str, str]:
            """通知一覧取得"""
            log.info("Notification endpoint")
            return {"message": "Notification endpoint (to be implemented)"}


# インスタンス化
user_api = UserAPI()
user_router = user_api.me_router
search_tag_router = user_api.search_tag_router
follow_router = user_api.follow_router
follower_router = user_api.follower_router
like_media_router = user_api.like_media_router
like_comment_router = user_api.like_comment_router
notification_router = user_api.notification_router
