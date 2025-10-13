from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from api.admin import manage_site
from api.routers import api


urlpatterns = [
    path("api/", include("api.urls")),
    path("api/ninja/", api.urls),
    path("api/auth/", include("rest_framework.urls")),
    path("", include("app.urls")),
    path("setting/", include("django.contrib.auth.urls")),
    path("myus-admin/", admin.site.urls),
    path("myus-manage/", manage_site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
    """ メディアファイルを扱う時の開発環境時の設定 """
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
