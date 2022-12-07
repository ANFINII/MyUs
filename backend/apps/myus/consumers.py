import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from apps.myus.views import ChatDetail, ChatThread, get_delta
from apps.myus.models import Chat, Message, Notification
from apps.myus.modules.contains import NotificationTypeNo

User = get_user_model()

class ChatConsumer(WebsocketConsumer):

    def create_message(self, data):
        chat = Chat.objects.get(id=data['chat_id'])
        delta = data['delta']
        html = data['message']
        message = Message.objects.create(
            chat=chat,
            author=self.scope['user'],
            text=html,
            delta=get_delta(delta, html),
        )
        chat.thread = chat.message.filter(parent__isnull=True).count()
        chat.joined = chat.message.values_list('author').distinct().count()
        chat.save(update_fields=['thread', 'joined'])
        content = {
            'command': 'create_message',
            'message': self.create_message_to_json(message)
        }
        return self.send_chat_message(content)

    def create_reply_message(self, data):
        user = self.scope['user']
        chat = Chat.objects.get(id=data['chat_id'])
        message = Message.objects.create(
            chat=chat,
            author=user,
            text=data['message'],
            parent_id=data['parent_id'],
        )
        author = message.parent.author
        chat.joined = chat.message.values_list('author').distinct().count()
        chat.save(update_fields=['joined'])
        parent = Message.objects.get(id=data['parent_id'])
        parent.reply_num = Message.objects.filter(parent=data['parent_id']).count()
        parent.save(update_fields=['reply_num'])
        if user != author and author.notificationsetting.is_reply:
            Notification.objects.create(
                user_from=user,
                user_to=author,
                type_no=NotificationTypeNo.reply,
                type_name='reply',
                content_object=message,
            )
        content = {
            'command': 'create_reply_message',
            'message': self.create_reply_message_to_json(message)
        }
        return self.send_chat_message(content)

    def update_message(self, data):
        message = Message.objects.get(id=data['message_id'])
        message.text = data['message']
        message.save(update_fields=['text', 'updated'])
        content = {
            'command': 'update_message',
            'message': self.update_message_to_json(message)
        }
        return self.send_chat_message(content)

    def delete_message(self, data):
        message = Message.objects.get(id=data['message_id'])
        content = {
            'command': 'delete_message',
            'message': self.delete_message_to_json(message)
        }
        message_dict = content['message']
        message_dict['message_id'] = data['message_id']
        return self.send_chat_message(content)

    def delete_reply_message(self, data):
        message = Message.objects.get(id=data['message_id'])
        content = {
            'command': 'delete_reply_message',
            'message': self.delete_reply_message_to_json(message)
        }
        message_dict = content['message']
        message_dict['message_id'] = data['message_id']
        return self.send_chat_message(content)

    def create_message_to_json(self, message):
        message_data = ChatDetail.get_message_data(self, message)
        context = {
            'user_id': self.scope['user'].id,
            'message_id': message.id,
            'joined': message_data['joined'],
            'thread': message_data['thread'],
            'message_lists': render_to_string('chat/chat_message/chat_message.html', {
                'user_id': self.scope['user'].id,
                'obj_id': message.chat_id,
                'message_id': message.id,
                'message_list': message_data['message'],
            })
        }
        return context

    def create_reply_message_to_json(self, message):
        reply_data = ChatThread.get_reply_data(self, message)
        context = {
            'user_id': self.scope['user'].id,
            'message_id': message.id,
            'parent_id': message.parent.id,
            'joined': reply_data['joined'],
            'reply_num': reply_data['reply_num'],
            'reply_lists': render_to_string('chat/chat_reply/chat_reply.html', {
                'user_id': self.scope['user'].id,
                'obj_id': message.chat_id,
                'reply_list': reply_data['reply'],
            })
        }
        return context

    def update_message_to_json(self, message):
        context = {
            'text': message.text,
            'message_id': message.id,
        }
        return context

    def delete_message_to_json(self, message):
        message.delete()
        chat = Chat.objects.get(id=message.chat_id)
        chat.thread = chat.message.filter(parent__isnull=True).count()
        chat.joined = chat.message.values_list('author').distinct().count()
        chat.save(update_fields=['thread', 'joined'])
        context = {
            'joined': chat.joined,
            'thread': chat.thread,
        }
        return context

    def delete_reply_message_to_json(self, message):
        Notification.objects.filter(type_no=NotificationTypeNo.reply, object_id=message.id).delete()
        message.delete()
        chat = Chat.objects.get(id=message.id)
        chat.joined = chat.message.values_list('author').distinct().count()
        chat.save(update_fields=['joined'])
        message = Message.objects.get(id=message.parent_id)
        message.reply_num = Message.objects.filter(parent=message.parent_id).count()
        message.save(update_fields=['reply_num'])
        context = {
            'joined': chat.joined,
            'parent_id': message.parent_id,
            'reply_num': message.reply_num,
        }
        return context

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

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {'type': 'chat_message', 'message': message}
        )

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    commands = {
        'create_message': create_message,
        'create_reply_message': create_reply_message,
        'update_message': update_message,
        'delete_message': delete_message,
        'delete_reply_message': delete_reply_message,
    }
