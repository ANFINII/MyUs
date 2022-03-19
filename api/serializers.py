from rest_framework import serializers
from api.models import User, MyPage, NotificationSetting, Notification, SearchTag, HashTag
from api.models import Video, Live, Music, Picture, Blog, Chat, Collabo
from api.models import Todo, Advertise, Follow, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'password', 'image', 'email', 'username', 'nickname', 'last_name', 'first_name',
            'birthday', 'gender', 'phone', 'location', 'introduction',
            'is_active', 'is_staff', 'is_admin', 'last_login', 'date_joined',
        )
        read_only_field = ['is_staff', 'is_admin', 'last_login', 'date_joined']


class MyPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyPage
        fields = (
            'id', 'user', 'banner', 'email', 'content', 'follow_num', 'follower_num',
            'rate_plan', 'rate_plan_date', 'auto_advertise',
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


class SearchTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchTag
        fields = ('id', 'author', 'sequence', 'name', 'created',)


class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = ('id', 'author', 'name', 'en_name',)


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = (
            'id', 'author', 'title', 'content', 'image', 'video', 'convert', 'comment',
            'tags', 'like', 'read', 'publish', 'created', 'updated',
        )


class LiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Live
        fields = (
            'id', 'author', 'title', 'content', 'image', 'live', 'comment',
            'tags', 'like', 'read', 'publish', 'created', 'updated',
        )


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = (
            'id', 'author', 'title', 'content', 'lyric', 'music', 'comment',
            'tags', 'like', 'read', 'download', 'publish', 'created', 'updated',
        )


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = (
            'id', 'author', 'title', 'content', 'image', 'comment',
            'tags', 'like', 'read', 'publish', 'created', 'updated',
        )


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = (
            'id', 'author', 'title', 'content', 'image', 'richtext', 'comment',
            'tags', 'like', 'read', 'publish', 'created', 'updated',
        )


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = (
            'id', 'author', 'title', 'content', 'comment', 'tags', 'like',
            'read', 'joined', 'period', 'publish', 'created', 'updated',
        )


class CollaboSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collabo
        fields = (
            'id', 'author', 'title', 'content', 'comment', 'tags', 'like',
            'read', 'period', 'publish', 'created', 'updated',
        )

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = (
            'id', 'author', 'title', 'content', 'priority', 'progress',
            'comment', 'duedate', 'created', 'updated',
        )


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('id', 'follower', 'following', 'created')


class AdvertiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertise
        fields = (
            'id', 'author', 'title', 'url', 'content', 'image', 'video',
            'read', 'type', 'period', 'publish', 'created', 'updated',
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id', 'author', 'parent', 'text', 'like', 'content_type',
            'object_id', 'content_object', 'created', 'updated',
        )
