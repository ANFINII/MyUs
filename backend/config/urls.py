"""config URL Configuration"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from apps.myus.admin import manage_site

urlpatterns = [
    path('', include('apps.myus.urls')),
    path('', include('apps.myus.api.urls')),
    path('', include('django.contrib.auth.urls')),
    path('myus-admin/', admin.site.urls),
    path('myus-manage/', manage_site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/auth/',include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    # path('api/auth/',include('djoser.urls.jwt')),
    # path('api/login/', TokenObtainPairView.as_view()),
    # path('api/refresh/', TokenRefreshView.as_view()),
    # path('api/verify/', TokenVerifyView.as_view()),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    """ メディアファイルを扱う時の開発環境時の設定 """
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
