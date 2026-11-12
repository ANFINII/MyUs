from django.http import HttpRequest
from api.db.models import User


class AdminBackend:
    """管理画面のログインに使う Backend。スタッフだけが username と email のどちらでもログインできる"""

    def authenticate(self, request: HttpRequest | None, username: str | None = None, password: str | None = None) -> User | None:
        if username is None or password is None:
            return None

        user = User.objects.filter(username=username, is_staff=True, is_active=True).first()
        if user is None:
            user = User.objects.filter(email=username, is_staff=True, is_active=True).first()

        if user is None or not user.check_password(password):
            return None

        return user

    def get_user(self, user_id: int) -> User | None:
        return User.objects.filter(id=user_id, is_staff=True, is_active=True).first()
