from typing import Any
from django.contrib import admin
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.models import Group
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import Count
from import_export.admin import ImportExportModelAdmin
from api.db.models import Notification, AccessLog, Comment, Message, Follow, Advertise, ComicPage
from api.db.models import User, Profile, MyPage, SearchTag, HashTag, Category, NgWord, UserNotification
from api.db.models import Video, Music, Blog, Comic, Picture, Chat


ADMIN_LOGIN_FAILURE_LIMIT = 5
ADMIN_LOGIN_LOCK_SECONDS = 60 * 60


class AdminLoginForm(AdminAuthenticationForm):
    def clean(self) -> dict[str, Any]:
        username = self.cleaned_data.get("username", "")
        cache_key = f"admin_login_failure:{username}"
        failure_count = cache.get(cache_key, 0)
        if failure_count >= ADMIN_LOGIN_FAILURE_LIMIT:
            raise ValidationError("ログインの失敗が続いたため、しばらくログインできません。1時間後にお試しください。")

        try:
            cleaned_data = super().clean()
        except ValidationError:
            cache.set(cache_key, failure_count + 1, ADMIN_LOGIN_LOCK_SECONDS)
            raise

        cache.delete(cache_key)
        return cleaned_data


# Admin用の管理画面
admin.site.login_form = AdminLoginForm
admin.site.site_title = "MyUs管理者画面"
admin.site.site_header = "MyUs管理者画面"
admin.site.index_title = "メニュー"
admin.site.unregister(Group)
admin.site.disable_action("delete_selected")


class ProfileInline(admin.StackedInline):
    model = Profile
    readonly_fields = ("country_code",)
    verbose_name = "プロファイル情報"

    def has_delete_permission(self, request, obj=None):
        return False


class MyPageInline(admin.StackedInline):
    model = MyPage
    readonly_fields = ("follower_count", "following_count", "tag_manager_id", "is_advertise")
    verbose_name = "マイページ情報"

    def has_delete_permission(self, request, obj=None):
        return False


class UserNotificationInline(admin.TabularInline):
    model = UserNotification
    verbose_name = "通知設定"

    def has_delete_permission(self, request, obj=None):
        return False


class SearchTagInline(admin.TabularInline):
    model = SearchTag
    extra = 1
    max_num = 20
    verbose_name_plural = "検索タグ"


# class CommentInlineAdmin(GenericTabularInline):
#     model = Comment
#     extra = 0
#     max_num = 100
#     exclude = ("like", "reply_count")
#     fields = ("author", "parent", "text", "total_like")
#     readonly_fields = ("total_like",)
#     verbose_name_plural = "コメント"

#     def total_like(self, obj):
#         return obj.like.count()
#     total_like.short_description = "いいね数"


class MessageInlineAdmin(admin.TabularInline):
    model = Message
    extra = 0
    max_num = 100
    exclude = ("reply_count",)
    fields = ("author", "parent", "text")
    verbose_name_plural = "メッセージ"


class ComicPageInlineAdmin(admin.StackedInline):
    model = ComicPage
    extra = 0
    max_num = 200
    readonly_fields = ("image", "sequence")
    verbose_name_plural = "コミックページ情報"

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    list_display = ("id", "email", "username", "nickname")
    search_fields = ("email", "username", "nickname")
    ordering = ("id",)
    filter_horizontal = ("groups", "user_permissions")
    readonly_fields = ("last_login", "date_joined")
    inlines = [ProfileInline, MyPageInline, UserNotificationInline, SearchTagInline]

    # 詳細画面
    fieldsets = [
        ("アカウント情報", {"fields": ("avatar", "email", "username", "nickname")}),
        ("権限情報", {"fields": ("is_active", "is_staff", "is_superuser", "last_login", "date_joined")}),
    ]


@admin.register(AccessLog)
class AccessLogAdmin(ImportExportModelAdmin):
    list_display = ("id", "ip_address", "type", "type_id", "created", "updated")
    search_fields = ("ip_address", "type", "type_id")
    ordering = ("id", "type", "type_id")
    readonly_fields = ("ip_address", "type", "created", "updated")

    # 詳細画面
    fieldsets = [
        ("確認項目", {"fields": ("ip_address", "type", "created", "updated")})
    ]


@admin.register(SearchTag)
class SearchTagAdmin(ImportExportModelAdmin):
    list_display = ("id", "author", "sequence", "name", "created")
    list_select_related = ("author",)
    list_per_page = 20
    search_fields = ("author__nickname", "name", "created")
    ordering = ("author", "sequence", "created")
    readonly_fields = ("author", "created")

    # 詳細画面
    fieldsets = [
        ("編集項目", {"fields": ("sequence", "name")}),
        ("確認項目", {"fields": ("author", "created")})
    ]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(SearchTagAdmin, self).save_model(request, obj, form, change)


@admin.register(HashTag)
class HashTagAdmin(ImportExportModelAdmin):
    list_display = ("id", "ulid", "name")
    list_editable = ("name",)
    search_fields = ("ulid", "name")
    ordering = ("id",)
    readonly_fields = ("ulid",)

    # 詳細画面
    fieldsets = [
        ("編集項目", {"fields": ("name",)}),
        ("確認項目", {"fields": ("ulid",)}),
    ]


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ("id", "ulid", "jp_name", "en_name")
    list_editable = ("jp_name", "en_name")
    search_fields = ("ulid", "jp_name", "en_name")
    ordering = ("id",)
    readonly_fields = ("ulid",)

    # 詳細画面
    fieldsets = [
        ("編集項目", {"fields": ("jp_name", "en_name")}),
        ("確認項目", {"fields": ("ulid",)}),
    ]


@admin.register(NgWord)
class NgWordAdmin(ImportExportModelAdmin):
    list_display = ("id", "word", "created")
    list_editable = ("word",)
    search_fields = ("word",)
    ordering = ("id",)
    readonly_fields = ("created",)

    # 詳細画面
    fieldsets = [
        ("編集項目", {"fields": ("word",)}),
        ("確認項目", {"fields": ("created",)}),
    ]


@admin.register(Video)
class VideoAdmin(ImportExportModelAdmin):
    list_display = ("id", "channel", "title", "read", "total_like", "comment_count", "score", "publish", "created", "updated")
    list_select_related = ("channel",)
    search_fields = ("title", "channel__owner__nickname", "created")
    ordering = ("channel", "-created")
    filter_horizontal = ("like",)
    readonly_fields = ("total_like", "comment_count", "created", "updated")
    # inlines = [CommentInlineAdmin]

    # 詳細画面
    fieldsets = [
        ("編集項目", {"fields": ("channel", "title", "content", "image", "video", "convert", "like", "read", "publish", "publish_at")}),
        ("確認項目", {"fields": ("total_like", "comment_count", "created", "updated")})
    ]


@admin.register(Music)
class MusicAdmin(ImportExportModelAdmin):
    list_display = ("id", "channel", "title", "read", "total_like", "comment_count", "download", "publish", "created", "updated")
    list_select_related = ("channel",)
    search_fields = ("title", "channel__owner__nickname", "created")
    ordering = ("channel", "-created")
    filter_horizontal = ("like",)
    readonly_fields = ("total_like", "comment_count", "created", "updated")
    # inlines = [CommentInlineAdmin]

    # 詳細画面
    fieldsets = [
        ("編集項目", {"fields": ("channel", "title", "content", "lyric", "music", "like", "read", "publish", "publish_at", "download")}),
        ("確認項目", {"fields": ("total_like", "comment_count", "created", "updated")})
    ]


@admin.register(Comic)
class ComicAdmin(ImportExportModelAdmin):
    list_display = ("id", "channel", "title", "read", "total_like", "comment_count", "publish", "created", "updated")
    list_select_related = ("channel",)
    search_fields = ("title", "channel__owner__nickname", "created")
    ordering = ("channel", "-created")
    filter_horizontal = ("like",)
    readonly_fields = ("total_like", "comment_count", "created", "updated")
    # inlines = [CommentInlineAdmin, ComicPageInlineAdmin]

    # 詳細画面
    fieldsets = [
        ("編集項目", {"fields": ("channel", "title", "content", "image", "like", "read", "publish", "publish_at")}),
        ("確認項目", {"fields": ("total_like", "comment_count", "created", "updated")})
    ]


@admin.register(Picture)
class PictureAdmin(ImportExportModelAdmin):
    list_display = ("id", "channel", "title", "read", "total_like", "comment_count", "publish", "created", "updated")
    list_select_related = ("channel",)
    search_fields = ("title", "channel__owner__nickname", "created")
    ordering = ("channel", "-created")
    filter_horizontal = ("like",)
    readonly_fields = ("total_like", "comment_count", "created", "updated")
    # inlines = [CommentInlineAdmin]

    # 詳細画面
    fieldsets = [
        ("編集項目", {"fields": ("channel", "title", "content", "image", "like", "read", "publish", "publish_at")}),
        ("確認項目", {"fields": ("total_like", "comment_count", "created", "updated")})
    ]


@admin.register(Blog)
class BlogAdmin(ImportExportModelAdmin):
    list_display = ("id", "channel", "title", "read", "total_like", "comment_count", "publish", "created", "updated")
    list_select_related = ("channel",)
    search_fields = ("title", "channel__owner__nickname", "created")
    ordering = ("channel", "-created")
    filter_horizontal = ("like",)
    readonly_fields = ("total_like", "comment_count", "created", "updated")
    # inlines = [CommentInlineAdmin]

    # 詳細画面
    fieldsets = [
        ("編集項目", {"fields": ("channel", "title", "content", "richtext", "image", "like", "read", "publish", "publish_at", "is_promotion")}),
        ("確認項目", {"fields": ("total_like", "comment_count", "created", "updated")})
    ]


@admin.register(Chat)
class ChatAdmin(ImportExportModelAdmin):
    list_display = ("id", "channel", "title", "read", "total_like", "thread_count", "joined_count", "period", "publish", "created", "updated")
    list_select_related = ("channel",)
    search_fields = ("title", "channel__owner__nickname", "created")
    ordering = ("channel", "-created")
    filter_horizontal = ("like",)
    readonly_fields = ("total_like", "thread_count", "joined_count", "created", "updated")
    inlines = [MessageInlineAdmin]

    # 詳細画面
    fieldsets = [
        ("編集項目", {"fields": ("channel", "title", "content", "like", "read", "period", "publish", "publish_at")}),
        ("確認項目", {"fields": ("total_like", "thread_count", "joined_count", "created", "updated")})
    ]


@admin.register(Follow)
class FollowAdmin(ImportExportModelAdmin):
    list_display = ("id", "follower", "following", "created")
    list_select_related = ("follower", "following")
    search_fields = ("follower__nickname", "following__nickname", "created")
    ordering = ("follower", "following", "-created")
    readonly_fields = ("created",)

    # 詳細画面
    fieldsets = [
        ("編集項目", {"fields": ("follower", "following")}),
        ("確認項目", {"fields": ("created",)})
    ]


@admin.register(Notification)
class NotificationAdmin(ImportExportModelAdmin):
    list_display = ("id", "user_from", "user_to", "type_no", "type_name", "object_id", "title", "confirmed_count", "deleted_count", "created")
    list_select_related = ("user_from", "user_to")
    search_fields = ("type_name", "created")
    ordering = ("type_no", "created")
    filter_horizontal = ("confirmed", "deleted")
    readonly_fields = ("title", "confirmed_count", "deleted_count", "created")

    # 詳細画面
    fieldsets = [
        ("編集項目", {"fields": ("user_from", "user_to", "type_no", "type_name", "object_id", "confirmed", "deleted")}),
        ("確認項目", {"fields": ("title", "confirmed_count", "deleted_count", "created")})
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("confirmed", "deleted")


@admin.register(Advertise)
class AdvertiseAdmin(ImportExportModelAdmin):
    list_display = ("id", "author", "title", "url", "read", "type", "period", "publish", "created", "updated")
    list_select_related = ("author",)
    search_fields = ("title", "author__nickname", "created")
    ordering = ("author", "created")
    readonly_fields = ("read", "created", "updated")

    # 詳細画面
    fieldsets = [
        ("編集項目", {"fields": ("author", "title", "url", "content", "image", "video", "type", "period", "publish")}),
        ("確認項目", {"fields": ("read", "created", "updated")})
    ]


@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin):
    list_display = ("id", "type_no", "type_name", "object_id", "author", "parent", "text", "total_like", "reply_count", "created", "updated")
    list_select_related = ("author", "parent")
    search_fields = ("text", "author__nickname", "created", "updated")
    ordering = ("created",)
    filter_horizontal = ("like",)
    readonly_fields = ("total_like", "reply_count", "created", "updated")

    # 詳細画面
    fieldsets = [
        ("編集項目", {"fields": ("author", "parent", "text", "like", "type_no", "type_name", "object_id")}),
        ("確認項目", {"fields": ("total_like", "reply_count", "created", "updated")})
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(reply_count=Count("reply"))


@admin.register(Message)
class MessageAdmin(ImportExportModelAdmin):
    list_display = ("id", "author", "chat", "parent", "text", "reply_count", "created", "updated")
    list_select_related = ("author", "chat", "parent")
    search_fields = ("text", "author__nickname", "created", "updated")
    ordering = ("created",)
    readonly_fields = ("reply_count", "created", "updated")

    # 詳細画面
    fieldsets = [
        ("編集項目", {"fields": ("author", "chat", "parent", "content")}),
        ("確認項目", {"fields": ("reply_count", "created", "updated")})
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(reply_count=Count("reply"))
