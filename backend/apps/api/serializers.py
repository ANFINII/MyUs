from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from apps.myus.models import Profile, MyPage, SearchTag, HashTag, NotificationSetting
from apps.myus.models import Notification, Follow, Comment, Message, Advertise
from apps.myus.models import Video, Live, Music, Picture, Blog, Chat, Collabo, Todo


User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    nickname = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    last_name = serializers.CharField()
    first_name = serializers.CharField()
    year = serializers.CharField()
    month = serializers.CharField()
    day = serializers.CharField()
    gender = serializers.IntegerField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'password', 'email', 'username', 'nickname',
            'is_active', 'is_staff', 'last_login', 'date_joined'
        )
        read_only_field = ['is_active', 'is_staff', 'last_login', 'date_joined']
        extra_kwargs = {
            'password':{
                'write_only': True,
                'required': True,
                'min_length': 8,
                'style': {'input_type': 'password'}
            }
        }


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'image', 'last_name', 'first_name', 'birthday', 'gender', 'phone', 'country_code',
            'postal_code', 'prefecture', 'city', 'address', 'building', 'introduction',
        )


class MyPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyPage
        fields = (
            'banner', 'email', 'content', 'follower_num', 'following_num',
            'plan', 'plan_date', 'is_advertise',
        )


class NotificationSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSetting
        fields = (
            'is_video', 'is_live', 'is_music', 'is_picture', 'is_blog', 'is_chat',
            'is_collabo', 'is_follow', 'is_reply', 'is_like', 'is_views',
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
            'id', 'author', 'title', 'content', 'hashtag', 'like', 'read',
            'joined', 'period', 'publish', 'created', 'updated',
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
            'id', 'author', 'parent', 'text', 'like', 'reply_num',
            'content_type', 'object_id', 'content_object', 'created', 'updated',
        )
        read_only_field = ['reply_num', 'created', 'updated']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'id', 'author', 'chat', 'parent', 'content', 'reply_num', 'created', 'updated',
        )
        read_only_field = ['reply_num', 'created', 'updated']
