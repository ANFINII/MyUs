from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps.myus.models import Profile, MyPage, SearchTag, HashTag, NotificationSetting, PlanMaster, UserPlan
from apps.myus.models import Notification, Follow, Comment, Message, Advertise
from apps.myus.models import Video, Music, Comic, Picture, Blog, Chat, Todo


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
            'id', 'avatar', 'password', 'email', 'username', 'nickname',
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
            'last_name', 'first_name', 'birthday', 'gender', 'phone', 'country_code',
            'postal_code', 'prefecture', 'city', 'street', 'building', 'introduction'
        )


class MyPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyPage
        fields = ('banner', 'email', 'content', 'follower_count', 'following_count', 'tag_manager_id', 'is_advertise')


class NotificationSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSetting
        fields = (
            'is_video', 'is_music', 'is_comic', 'is_picture', 'is_blog',
            'is_chat', 'is_follow', 'is_reply', 'is_like', 'is_views'
        )


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'id', 'user_from', 'user_to', 'type_no', 'type_name', 'content_type',
            'object_id', 'content_object', 'confirmed', 'deleted', 'created'
        )
        read_only_field = ['created',]


class PlanMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanMaster
        fields = ('id', 'name', 'stripe_api_id', 'price', 'max_advertise', 'description')


class UserPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPlan
        fields = ('id', 'plan', 'start_date', 'end_date', 'is_free')


class SearchTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchTag
        fields = ('id', 'author', 'sequence', 'name', 'created')
        read_only_field = ['created',]


class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = ('id', 'author', 'jp_name', 'en_name')


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = (
            'id', 'author', 'title', 'content', 'image', 'video', 'convert',
            'hashtag', 'like', 'read', 'publish', 'created', 'updated'
        )
        read_only_field = ['created', 'updated']


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = (
            'id', 'author', 'title', 'content', 'lyric', 'music', 'hashtag',
            'like', 'read', 'download', 'publish', 'created', 'updated'
        )
        read_only_field = ['created', 'updated']


class ComicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comic
        fields = (
            'id', 'author', 'title', 'content', 'hashtag', 'like',
            'read', 'period', 'publish', 'created', 'updated'
        )
        read_only_field = ['created', 'updated']


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = (
            'id', 'author', 'title', 'content', 'image', 'hashtag',
            'like', 'read', 'publish', 'created', 'updated'
        )
        read_only_field = ['created', 'updated']


class BlogSerializer(serializers.ModelSerializer):
    # image = serializers.FileField()
    # image = serializers.ImageField(use_url=True)
    image = serializers.ImageField()
    class Meta:
        # model = Blog
        # fields = (
        #     'id', 'author', 'title', 'content', 'richtext', 'image',
        #     'hashtag', 'like', 'read', 'publish', 'created', 'updated'
        # )
        fields = (
            'title', 'content', 'richtext'
            # 'created', 'updated'
        )
        # read_only_field = ['created', 'updated']


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = (
            'id', 'author', 'title', 'content', 'hashtag', 'like', 'read',
            'joined', 'period', 'publish', 'created', 'updated'
        )
        read_only_field = ['created', 'updated']


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'author', 'title', 'content', 'priority', 'progress', 'duedate', 'created', 'updated')
        read_only_field = ['created', 'updated']


class AdvertiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertise
        fields = (
            'id', 'author', 'title', 'url', 'content', 'image', 'video',
            'read', 'type', 'period', 'publish', 'created', 'updated'
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
            'id', 'author', 'parent', 'text', 'like', 'reply_count',
            'content_type', 'object_id', 'content_object', 'created', 'updated'
        )
        read_only_field = ['reply_count', 'created', 'updated']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'author', 'chat', 'parent', 'content', 'reply_count', 'created', 'updated')
        read_only_field = ['reply_count', 'created', 'updated']
