"""config URL Configuration"""
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from myusapp.admin import mypage_site
from django.contrib.auth.models import Group
from ckeditor_uploader import views

urlpatterns = [
    path('myus-admin/', admin.site.urls),
    path('mypage/', mypage_site.urls),
    # path('markdownx/', include('markdownx.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('myusapp.urls')),
    path('', include("django.contrib.auth.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    """ メディアファイルを扱う時の開発環境時の設定 """
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_title = 'MyUs管理者画面'
admin.site.site_header = 'MyUs管理者画面'
admin.site.index_title = 'メニュー'
admin.site.unregister(Group)
admin.site.disable_action('delete_selected')