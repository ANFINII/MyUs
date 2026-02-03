from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password


User = get_user_model()

class MyBackend:
    """Custom authentication Backend username and email"""
    def authenticate(self, request, username, password):
        user = User.objects.filter(username=username).first()
        if not user:
            user = User.objects.filter(email=username).first()

        if user and check_password(password, user.password):
            return user
        return None

    def get_user(self, user_id):
        return User.objects.filter(id=user_id).first()
