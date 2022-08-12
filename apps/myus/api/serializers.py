from rest_framework import serializers
from apps.myus.models import User, MyPage, SearchTag, HashTag, NotificationSetting
from apps.myus.models import Notification, Follow, Comment, Advertise
from apps.myus.models import Video, Live, Music, Picture, Blog, Chat, Collabo, Todo


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'password', 'image', 'email', 'username', 'nickname', 'last_name', 'first_name',
            'birthday', 'gender', 'phone', 'location', 'introduction',
            'is_active', 'is_staff', 'is_admin', 'last_login', 'date_joined',
        )
        read_only_field = ['is_staff', 'is_admin', 'last_login', 'date_joined']
        extra_kwargs = {
            'password':{
                'write_only': True,
                'required': True,
                'min_length': 8,
                'style': {'input_type': 'password'}
            }
        }


class MyPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyPage
        fields = (
            'id', 'user', 'banner', 'email', 'content', 'follower_num', 'following_num',
            'plan', 'plan_date', 'is_advertise',
        )


class NotificationSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSetting
        fields = (
            'id', 'user', 'is_video', 'is_live', 'is_music', 'is_picture', 'is_blog',
            'is_chat', 'is_collabo', 'is_follow', 'is_reply', 'is_like', 'is_views',
        )


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'id', 'user_from', 'user_to', 'type_no', 'type_name', 'content_type',
            'object_id', 'content_object', 'confirmed', 'deleted', 'created',
        )
        read_only_field = ['created',]


class SearchTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchTag
        fields = ('id', 'author', 'sequence', 'name', 'created',)
        read_only_field = ['created',]


class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = ('id', 'author', 'jp_name', 'en_name',)


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = (
            'id', 'author', 'title', 'content', 'image', 'video', 'convert', 'comment',
            'hashtag', 'like', 'read', 'publish', 'created', 'updated',
        )
        read_only_field = ['created', 'updated']


class LiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Live
        fields = (
            'id', 'author', 'title', 'content', 'image', 'live', 'comment',
            'hashtag', 'like', 'read', 'publish', 'created', 'updated',
        )
        read_only_field = ['created', 'updated']


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = (
            'id', 'author', 'title', 'content', 'lyric', 'music', 'comment',
            'hashtag', 'like', 'read', 'download', 'publish', 'created', 'updated',
        )
        read_only_field = ['created', 'updated']


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = (
            'id', 'author', 'title', 'content', 'image', 'comment',
            'hashtag', 'like', 'read', 'publish', 'created', 'updated',
        )
        read_only_field = ['created', 'updated']


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = (
            'id', 'author', 'title', 'content', 'image', 'richtext', 'comment',
            'hashtag', 'like', 'read', 'publish', 'created', 'updated',
        )
        read_only_field = ['created', 'updated']


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = (
            'id', 'author', 'title', 'content', 'comment', 'hashtag',
            'like', 'read', 'joined', 'period', 'publish', 'created', 'updated',
        )
        read_only_field = ['created', 'updated']


class CollaboSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collabo
        fields = (
            'id', 'author', 'title', 'content', 'comment', 'hashtag',
            'like', 'read', 'period', 'publish', 'created', 'updated',
        )
        read_only_field = ['created', 'updated']


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = (
            'id', 'author', 'title', 'content', 'priority', 'progress',
            'comment', 'duedate', 'created', 'updated',
        )
        read_only_field = ['created', 'updated']


class AdvertiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertise
        fields = (
            'id', 'author', 'title', 'url', 'content', 'image', 'video',
            'read', 'type', 'period', 'publish', 'created', 'updated',
        )
        read_only_field = ['created', 'updated']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('id', 'follower', 'following', 'created')
        read_only_field = ['created',]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id', 'author', 'parent', 'text', 'like', 'content_type',
            'object_id', 'content_object', 'created', 'updated',
        )
        read_only_field = ['created', 'updated']