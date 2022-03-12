from rest_framework import serializers
from api.models import User, MyPage, NotificationSetting, Notification, SearchTag, HashTag
from api.models import VideoModel, LiveModel, MusicModel, PictureModel, BlogModel, ChatModel, CollaboModel
from api.models import TodoModel, FollowModel, AdvertiseModel, CommentModel


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
        model = VideoModel
        fields = (
            'id', 'author', 'title', 'content', 'images', 'videos', 'convert', 'comments',
            'publish', 'tags', 'like', 'read', 'created', 'updated',
        )


class LiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveModel
        fields = (
            'id', 'author', 'title', 'content', 'images', 'lives', 'comments',
            'publish', 'tags', 'like', 'read', 'created', 'updated',
        )


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicModel
        fields = (
            'id', 'author', 'title', 'content', 'lyrics', 'musics', 'comments',
            'publish', 'download', 'tags', 'like', 'read', 'created', 'updated',
        )


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PictureModel
        fields = (
            'id', 'author', 'title', 'content', 'images', 'comments',
            'publish', 'tags', 'like', 'read', 'created', 'updated',
        )


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogModel
        fields = (
            'id', 'author', 'title', 'content', 'images', 'richtext', 'comments',
            'publish', 'tags', 'like', 'read', 'created', 'updated',
        )


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatModel
        fields = (
            'id', 'author', 'title', 'content', 'comments', 'publish', 'tags',
            'like', 'read', 'joined', 'period', 'created', 'updated',
        )


class CollaboSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollaboModel
        fields = (
            'id', 'author', 'title', 'content', 'comments', 'publish',
            'tags', 'like', 'read', 'period', 'created', 'updated',
        )

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoModel
        fields = (
            'id', 'author', 'title', 'content', 'priority', 'progress',
            'comments', 'duedate', 'created', 'updated',
        )


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowModel
        fields = ('id', 'follower', 'following', 'created')


class AdvertiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertiseModel
        fields = (
            'id', 'author', 'title', 'url', 'content', 'images', 'videos', 'publish',
            'read', 'type', 'period', 'created', 'updated',
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = (
            'id', 'author', 'parent', 'text', 'like', 'content_type',
            'object_id', 'content_object', 'created', 'updated',
        )
