"""config URL Configuration"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from ckeditor_uploader import views
from apps.myus.admin import manage_site

urlpatterns = [
    path('', include('apps.myus.urls')),
    path('', include('django.contrib.auth.urls')),
    path('myus-admin/', admin.site.urls),
    path('myus-manage/', manage_site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('api-token-verify/', verify_jwt_token),
    path('upload/', login_required(views.upload), name='ckeditor_upload'),
    path('browse/', never_cache(login_required(views.browse)), name='ckeditor_browse'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    """ メディアファイルを扱う時の開発環境時の設定 """
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
