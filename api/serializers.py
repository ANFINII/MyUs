from rest_framework import serializers
from api.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'password', 'user_image', 'email', 'username', 'nickname', 'last_name', 'first_name',
            'birthday', 'gender', 'phone', 'location', 'introduction',
            'is_active', 'is_staff', 'is_admin', 'last_login', 'date_joined',
        )
