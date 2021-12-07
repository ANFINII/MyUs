import json
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.template.defaultfilters import linebreaksbr
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import ChatModel, CommentModel, NotificationModel
from .views import ChatDetail, ChatThread

User = get_user_model()

class ChatConsumer(WebsocketConsumer):
    def create_message(self, data):
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
        return self.send_chat_message(content)

    def create_reply_message(self, data):
        obj = ChatModel.objects.get(id=data['obj_id'])
        message = CommentModel.objects.create(
            author_id=self.scope['user'].id,
            text=data['message'],
            content_object=obj,
            parent_id=data['parent_id'],
            )
        NotificationModel.objects.create(
            user_from_id=self.scope['user'].id,
            user_to_id=message.parent.author.id,
            type_no=10,
            content_object=message,
        )
        content = {
            'command': 'create_reply_message',
            'message': self.create_reply_message_to_json(message)
        }
        return self.send_chat_message(content)

    def update_message(self, data):
        message = CommentModel.objects.get(id=data['comment_id'])
        message.text = data['message']
        message.save()
        content = {
            'command': 'update_message',
            'message': self.update_message_to_json(message)
        }
        return self.send_chat_message(content)

    def delete_message(self, data):
        message = CommentModel.objects.get(id=data['comment_id'])
        message.delete()
        content = {
            'command': 'delete_message',
            'message': self.delete_message_to_json(message)
        }
        message_dict = content['message']
        message_dict['comment_id'] = data['comment_id']
        return self.send_chat_message(content)

    def delete_reply_message(self, data):
        message = CommentModel.objects.get(id=data['comment_id'])
        content = {
            'command': 'delete_reply_message',
            'message': self.delete_reply_message_to_json(message)
        }
        message_dict = content['message']
        message_dict['comment_id'] = data['comment_id']
        return self.send_chat_message(content)

    def create_message_to_json(self, message):
        comment_list = ChatDetail.get_new_message(self, message)
        context = {
            'user_id': self.scope['user'].id,
            'comment_id': message.id,
            'user_count': comment_list['user_count'],
            'comment_count': comment_list['comment_count'],
            'comment_lists': render_to_string('chat/chat_comment/chat_comment.html', {
                'user_id': self.scope['user'].id,
                'obj_id': message.object_id,
                'comment_id': message.id,
                'comment_list': comment_list['comment_list'],
            })
        }
        return context

    def create_reply_message_to_json(self, message):
        reply_list = ChatThread.get_new_reply(self, message)
        context = {
            'user_id': self.scope['user'].id,
            'comment_id': message.id,
            'parent_id': message.parent.id,
            'user_count': reply_list['user_count'],
            'reply_count': reply_list['reply_count'],
            'reply_lists': render_to_string('chat/chat_reply/chat_reply.html', {
                'user_id': self.scope['user'].id,
                'obj_id': message.object_id,
                'reply_list': reply_list['reply_list'],
            })
        }
        return context

    def update_message_to_json(self, message):
        context = {
            'text': linebreaksbr(message.text),
            'comment_id': message.id,
        }
        return context

    def delete_message_to_json(self, message):
        obj_id = message.object_id
        obj = ChatModel.objects.get(id=obj_id)
        context = {
            'user_count': obj.user_count(),
            'comment_count': obj.comment_count(),
        }
        return context

    def delete_reply_message_to_json(self, message):
        obj_id = message.object_id
        obj = ChatModel.objects.get(id=obj_id)
        comment_obj = CommentModel.objects.get(id=message.id)
        message.delete()
        context = {
            'user_count': obj.user_count(),
            'parent_id': comment_obj.parent_id,
            'reply_count': comment_obj.parent.replies_count(),
        }
        return context

    commands = {
        'create_message': create_message,
        'create_reply_message': create_reply_message,
        'update_message': update_message,
        'delete_message': delete_message,
        'delete_reply_message': delete_reply_message,
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
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
