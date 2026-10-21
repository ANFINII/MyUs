import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.urls import path
from api.modules.logger import log
from api.src.usecase.media import is_public_chat


class ChatConsumer(WebsocketConsumer):
    def connect(self) -> None:
        ulid = self.scope["url_route"]["kwargs"]["ulid"]
        self.room_group_name = f"chat_detail_{ulid}"

        ret = is_public_chat(ulid)
        if ret.is_err:
            self.close()
            return

        is_public = ret.ok_value
        if not is_public:
            log.warning("WebSocket chat not found", ulid=ulid)
            self.close()
            return

        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

    def disconnect(self, code: int) -> None:
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def chat_message(self, event: dict[str, object]) -> None:
        self.send(text_data=json.dumps(event["message"]))


websocket_urlpatterns = [
    path("ws/chat/detail/<ulid>", ChatConsumer.as_asgi()),
]
