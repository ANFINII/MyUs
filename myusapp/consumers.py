import json
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import ChatModel, CommentModel

User = get_user_model()

class ChatConsumer(WebsocketConsumer):
    def fetch_message(self, data):
        print('fetch')
        messages = CommentModel.get_message()
        content = {
            'command': 'messages',
            'messages': self.fetch_messages_to_json(messages)
        }
        self.send_message(content)

    def create_message(self, data):
        print('create_message')
        print(data)
        user = User.objects.get(id=data['user_id'])
        obj = ChatModel.objects.get(id=data['obj_id'])
        message = CommentModel.objects.create(
            author=user,
            text=data['message'],
            content_object = obj,
            )
        content = {
            'command': 'create_message',
            'message': self.message_to_json(message)
        }
        print('create content:')
        print(content)
        return self.send_chat_message(content)

    def fetch_messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        print('message_to_json:')
        print(message)
        return {
            'text': message.text,
            'obj_id': message.object_id,
            'comment_id': message.id,
            'user_id': message.author.id,
            'nickname': message.author.nickname,
            'user_image': message.author.user_image.url,
            'created': str(message.created.strftime("%Y/%m/%d %H:%M")),
        }

    commands = {
        'fetch_message': fetch_message,
        'create_message': create_message,
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = 'chat_detail_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        print('receive')
        print(data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        print('send_chat_message:')
        print(message)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']
        print('chat_message_event')
        print(event)
        print('chat_message')
        print(message)

        self.send(text_data=json.dumps(message))

    def send_message(self, message):
        print('send_message:')
        print(message)
        self.send(text_data=json.dumps(message))


class ChatThereadConsumer(WebsocketConsumer):
    def connect(self):
        self.comment_id = self.scope['url_route']['kwargs']['comment_id']
        self.room_group_name = 'chat_detail_thread_%s' % self.comment_id
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
