from django.urls import path
from myusapp.consumers import ChatConsumer, ChatThereadConsumer

websocket_urlpatterns = [
    path('ws/chat/detail/<pk>', ChatConsumer.as_asgi()),
    path('ws/chat/detail/thread/<comment_id>', ChatThereadConsumer.as_asgi()),
]
