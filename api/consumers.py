import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.template.defaultfilters import linebreaksbr
from api.views import ChatDetail, ChatThread
from api.models import Chat, Comment, Notification
from api.modules.contains import NotificationTypeNo

User = get_user_model()

class ChatConsumer(WebsocketConsumer):
    def create_message(self, data):
        obj = Chat.objects.get(id=data['obj_id'])
        message = Comment.objects.create(
            author=self.scope['user'],
            text=data['message'],
            content_object=obj,
        )
        obj.thread = obj.comment.filter(parent__isnull=True).count()
        obj.joined = obj.comment.values_list('author').distinct().count()
        obj.save(update_fields=['thread', 'joined'])
        content = {
            'command': 'create_message',
            'message': self.create_message_to_json(message)
        }
        return self.send_chat_message(content)

    def create_reply_message(self, data):
        user = self.scope['user']
        obj = Chat.objects.get(id=data['obj_id'])
        message = Comment.objects.create(
            author=user,
            text=data['message'],
            content_object=obj,
            parent_id=data['parent_id'],
        )
        author = message.parent.author
        obj.joined = obj.comment.values_list('author').distinct().count()
        obj.save(update_fields=['joined'])
        parent_obj = Comment.objects.get(id=data['parent_id'])
        parent_obj.reply_num = Comment.objects.filter(parent=data['parent_id']).count()
        parent_obj.save(update_fields=['reply_num'])
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
        message = Comment.objects.get(id=data['comment_id'])
        message.text = data['message']
        message.save(update_fields=['text', 'updated'])
        content = {
            'command': 'update_message',
            'message': self.update_message_to_json(message)
        }
        return self.send_chat_message(content)

    def delete_message(self, data):
        message = Comment.objects.get(id=data['comment_id'])
        content = {
            'command': 'delete_message',
            'message': self.delete_message_to_json(message)
        }
        message_dict = content['message']
        message_dict['comment_id'] = data['comment_id']
        return self.send_chat_message(content)

    def delete_reply_message(self, data):
        message = Comment.objects.get(id=data['comment_id'])
        content = {
            'command': 'delete_reply_message',
            'message': self.delete_reply_message_to_json(message)
        }
        message_dict = content['message']
        message_dict['comment_id'] = data['comment_id']
        return self.send_chat_message(content)

    def create_message_to_json(self, message):
        message_data = ChatDetail.get_message_data(self, message)
        context = {
            'user_id': self.scope['user'].id,
            'comment_id': message.id,
            'joined': message_data['joined'],
            'thread': message_data['thread'],
            'comment_lists': render_to_string('chat/chat_comment/chat_comment.html', {
                'user_id': self.scope['user'].id,
                'obj_id': message.object_id,
                'comment_id': message.id,
                'comment_list': message_data['comment_obj'],
            })
        }
        return context

    def create_reply_message_to_json(self, message):
        reply_data = ChatThread.get_reply_data(self, message)
        context = {
            'user_id': self.scope['user'].id,
            'comment_id': message.id,
            'parent_id': message.parent.id,
            'joined': reply_data['joined'],
            'reply_num': reply_data['reply_num'],
            'reply_lists': render_to_string('chat/chat_reply/chat_reply.html', {
                'user_id': self.scope['user'].id,
                'obj_id': message.object_id,
                'reply_list': reply_data['reply_obj'],
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
        message.delete()
        obj = Chat.objects.get(id=message.object_id)
        obj.thread = obj.comment.filter(parent__isnull=True).count()
        obj.joined = obj.comment.values_list('author').distinct().count()
        obj.save(update_fields=['thread', 'joined'])
        context = {
            'joined': obj.joined,
            'thread': obj.thread,
        }
        return context

    def delete_reply_message_to_json(self, message):
        Notification.objects.filter(type_no=NotificationTypeNo.reply, object_id=message.id).delete()
        message.delete()
        obj = Chat.objects.get(id=message.object_id)
        obj.joined = obj.comment.values_list('author').distinct().count()
        obj.save(update_fields=['joined'])
        comment_obj = Comment.objects.get(id=message.parent_id)
        comment_obj.reply_num = Comment.objects.filter(parent=message.parent_id).count()
        comment_obj.save(update_fields=['reply_num'])
        context = {
            'joined': obj.joined,
            'parent_id': message.parent_id,
            'reply_num': comment_obj.reply_num,
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
            self.room_group_name, {'type': 'chat_message', 'message': message}
        )

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
