from rest_framework import serializers
from api.models import User, MyPage, NotificationSetting, Notification, SearchTagModel, TagModel
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
            'id', 'user', 'image', 'email', 'content', 'follower_num', 'follow_num',
            'rate_plan', 'rate_plan_date', 'auto_advertise',
        )

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'id', 'user', 'image', 'email', 'content', 'follower_num', 'follow_num',
            'rate_plan', 'rate_plan_date', 'auto_advertise',
        )
