from rest_framework import serializers
from api.models import User


class UserSerializer(serializers.ModelSerializer):
    notification = serializers.SerializerMethodField()
    profile_src = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'email',
            'is_active',
            'is_deleted',
            'last_login',
            'role',
            'password',
            'profile_src',
            'notification',
        )

    def get_notification(self, obj):
        notifications = obj.notification
        return notifications[0] if notifications and len(notifications) > 0 else None

    def get_profile_src(self, obj):
        return obj.profile.url if obj.profile else ''
