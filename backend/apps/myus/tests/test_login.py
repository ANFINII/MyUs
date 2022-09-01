from django.test import TestCase
from django.test import Client
from django.contrib.auth import authenticate, get_user_model

# Create your tests here.

User = get_user_model()

class LoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='emailtest@gmail.com',
            username='usernametest',
            nickname='nicknametest',
            password='passwordtest',
            is_active=True,
        )

    def test_login_success(self):
        client = Client()
        response = client.get('/') # ログインしない状態でアクセス
        self.assertEqual(response.status_code, 200) # ステータスコード：200が返却され画面にアクセスできる
        username = 'usernametest'
        password = 'passwordtest'

        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active or user.is_staff:
                    login = client.login(username=username, password=password)
                    self.assertTrue(login, 'ログイン成功')
                    response = client.get('/')
                    self.assertEqual(response.status_code, 200) # ログインした状態でアクセス
                    client.logout()
                else:
                    self.assertTrue(self.login, 'ID又はパスワードが違います!')
                    response = client.get('http://localhost:8000/login/')
                    self.assertEqual(response.status_code, 200)
            else:
                self.assertTrue(self.login, 'ID又はパスワードが違います!')
                response = client.get('http://localhost:8000/login/')
                self.assertEqual(response.status_code, 200)
        except User.DoesNotExist:
            self.assertTrue(login, 'IDが違います!')
