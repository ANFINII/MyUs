from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path
from config.views import serve_media
from myus.adapter.inbound.routers import api


urlpatterns: list[URLPattern | URLResolver] = [
    path("api/", api.urls),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.insert(0, path("__debug__/", include(debug_toolbar.urls)))
    """ メディアファイルを扱う時の開発環境時の設定 """
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [path("media/<path:path>", serve_media)]
