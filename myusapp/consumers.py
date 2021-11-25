import json
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import ChatModel, CommentModel
from .views import ChatDetail

User = get_user_model()

class ChatConsumer(WebsocketConsumer):
    def fetch_message(self, data):
        print('fetch_message:')
        messages = ChatDetail.get_chat_message(data['obj_id'])
        content = {
            'command': 'fetch_message',
            'messages': self.fetch_message_to_json(messages)
        }
        print(content)
        self.send_message(content)

    def create_message(self, data):
        print('create_message:')
        print(data)
        obj = ChatModel.objects.get(id=data['obj_id'])
        message = CommentModel.objects.create(
            author_id=self.scope['user'].id,
            text=data['message'],
            content_object = obj,
            )
        content = {
            'command': 'create_message',
            'message': self.create_message_to_json(message)
        }
        print('create content:')
        print(content)
        return self.send_chat_message(content)

    def update_message(self, data):
        print('update_message:')
        print(data)
        message = CommentModel.objects.get(id=data['comment_id'])
        message.text = data['message']
        message.save()
        print(message)
        content = {
            'command': 'update_message',
            'message': self.update_message_to_json(message)
        }
        print('update content:')
        print(content)
        return self.send_chat_message(content)

    def delete_message(self, data):
        print('delete_message:')
        print(data)
        message = CommentModel.objects.get(id=data['comment_id'])
        print(message)
        message.delete()
        content = {
            'command': 'delete_message',
            'message': self.delete_message_to_json(message)
        }
        message_dict = content['message']
        message_dict['comment_id'] = data['comment_id']
        print('delete content:')
        print(content)
        return self.send_chat_message(content)


    def fetch_message_to_json(self, messages):
        print('fetch_messages_to_json:')
        print(messages)
        result = []
        for message in messages:
            result.append(self.fetch_message_json(message))
        return result

    def fetch_message_json(self, message):
        print('fetch_message_json:')
        print(message)
        context = {
            'comment_id': message.id,
            'author': message.author.nickname,
            'text': message.text,
            'created': str(message.created)
        }
        print(context)
        return context

    def create_message_to_json(self, message):
        print('create_message_to_json:')
        print(message)
        comment_list = ChatDetail.get_new_message(self, message)
        context = {
            'user_count': comment_list['user_count'],
            'comment_count': comment_list['comment_count'],
            'comment_lists': render_to_string('chat/chat_comment/chat_comment.html', {

                'obj_id': message.object_id,
                'comment_id': message.id,
                'comment_list': comment_list['comment_list'],
            })
        }
        return context

    def update_message_to_json(self, message):
        print('update_message_to_json:')
        print(message)
        context = {
            'text': message.text,
            'comment_id': message.id,
        }
        return context

    def delete_message_to_json(self, message):
        print('delete_message_to_json:')
        print(message)
        obj_id = message.object_id
        obj = ChatModel.objects.get(id=obj_id)
        context = {
            'user_count': obj.user_count(),
            'comment_count': obj.comment_count(),
        }
        return context

    commands = {
        'fetch_message': fetch_message,
        'create_message': create_message,
        'update_message': update_message,
        'delete_message': delete_message,
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
                'message': message,
            }
        )

    def chat_message(self, event):
        message = event['message']
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
