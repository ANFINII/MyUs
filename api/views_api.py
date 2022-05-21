from django.contrib.auth import authenticate, get_user_model, login, logout
from django.http import JsonResponse
from rest_framework import authentication, permissions, views
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from api.serializers import UserSerializer


# Create your views here.

User = get_user_model()

class SignUpAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class Login(views.APIView):
    pass

class Index(views.APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        nicknames = [user.nickname for user in User.objects.all()]
        return Response(nicknames)

    def post(self, request):
        # 普通こんなことはしないが..
        users = [User(username=username) for username in request.POST.getlist('username')]
        User.objects.bulk_create(users)
        return Response({'succeeded': True})


def PingView(request):
    return JsonResponse({'result': True})
