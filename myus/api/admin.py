import json
from import_export.admin import ImportExportModelAdmin
from django.db.models import Count
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib.contenttypes.admin import GenericTabularInline
from myus.api.models import User, Profile, MyPage, SearchTag, HashTag, UserNotification
from myus.api.models import Notification, AccessLog, Comment, Message, Follow, Advertise, ComicPage
from myus.api.models import Video, Music, Comic, Picture, Blog, Chat, Todo


# Admin用の管理画面
admin.site.site_title = 'MyUs管理者画面'
admin.site.site_header = 'MyUs管理者画面'
admin.site.index_title = 'メニュー'
admin.site.unregister(Group)
admin.site.disable_action('delete_selected')


class ProfileInline(admin.StackedInline):
    model = Profile
    readonly_fields = ('country_code',)
    verbose_name = 'プロファイル情報'

    def has_delete_permission(self, request, obj=None):
        return False


class MyPageInline(admin.StackedInline):
    model = MyPage
    readonly_fields = ('follower_count', 'following_count', 'tag_manager_id', 'is_advertise')
    verbose_name = 'マイページ情報'

    def has_delete_permission(self, request, obj=None):
        return False


class UserNotificationInline(admin.TabularInline):
    model = UserNotification
    verbose_name = '通知設定'

    def has_delete_permission(self, request, obj=None):
        return False


class SearchTagInline(admin.TabularInline):
    model = SearchTag
    extra = 1
    max_num = 20
    verbose_name_plural = '検索タグ'


class CommentInlineAdmin(GenericTabularInline):
    model = Comment
    extra = 0
    max_num = 100
    exclude = ('like', 'reply_count')
    fields = ('author', 'parent', 'text', 'total_like')
    readonly_fields = ('total_like',)
    verbose_name_plural = 'コメント'

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'いいね数'


class MessageInlineAdmin(admin.TabularInline):
    model = Message
    extra = 0
    max_num = 100
    exclude = ('reply_count',)
    fields = ('author', 'parent', 'text')
    verbose_name_plural = 'メッセージ'


class ComicPageInlineAdmin(admin.StackedInline):
    model = ComicPage
    extra = 0
    max_num = 200
    readonly_fields = ('image', 'sequence')
    verbose_name_plural = 'コミックページ情報'

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    list_display = ('id', 'email', 'username', 'nickname', 'full_name', 'birthday', 'age', 'gender', 'plan')
    search_fields = ('email', 'username', 'nickname', 'full_name', 'age', 'gender', 'plan')
    ordering = ('id',)
    filter_horizontal = ('groups', 'user_permissions')
    readonly_fields = ('last_login', 'date_joined')
    inlines = [ProfileInline, MyPageInline, UserNotificationInline, SearchTagInline]

    # 詳細画面
    fieldsets = [
        ('アカウント情報', {'fields': ('avatar', 'email', 'username', 'nickname')}),
        ('権限情報', {'fields': ('is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined')}),
    ]


@admin.register(AccessLog)
class AccessLogAdmin(ImportExportModelAdmin):
    list_display = ('id', 'ip_address', 'type', 'type_id', 'created', 'updated')
    search_fields = ('ip_address', 'type', 'type_id')
    ordering = ('id', 'type', 'type_id')
    readonly_fields = ('ip_address', 'type', 'created', 'updated')

    # 詳細画面
    fieldsets = [
        ('確認項目', {'fields': ('ip_address', 'type', 'created', 'updated')})
    ]


@admin.register(SearchTag)
class SearchTagAdmin(ImportExportModelAdmin):
    list_display = ('id', 'author', 'sequence', 'name', 'created')
    list_select_related = ('author',)
    list_per_page = 20
    search_fields = ('author__nickname', 'name', 'created')
    ordering = ('author', 'sequence', 'created')
    readonly_fields = ('author', 'created')

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('sequence', 'name')}),
        ('確認項目', {'fields': ('author', 'created')})
    ]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(SearchTagAdmin, self).save_model(request, obj, form, change)


@admin.register(HashTag)
class HashTagAdmin(ImportExportModelAdmin):
    list_display = ('id', 'jp_name', 'en_name')
    list_editable = ('jp_name', 'en_name')
    search_fields = ('jp_name', 'en_name')
    ordering = ('id',)

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('jp_name', 'en_name')}),
    ]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(HashTagAdmin, self).save_model(request, obj, form, change)


@admin.register(Video)
class VideoAdmin(ImportExportModelAdmin):
    list_display = ('id', 'author', 'title', 'read', 'total_like', 'comment_count', 'score', 'publish', 'created', 'updated')
    list_select_related = ('author',)
    search_fields = ('title', 'author__nickname', 'created')
    ordering = ('author', '-created')
    filter_horizontal = ('hashtag', 'like')
    readonly_fields = ('total_like', 'comment_count', 'created', 'updated')
    inlines = [CommentInlineAdmin]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('author', 'title', 'content', 'image', 'video', 'convert', 'hashtag', 'like', 'read', 'publish')}),
        ('確認項目', {'fields': ('total_like', 'comment_count', 'created', 'updated')})
    ]


@admin.register(Music)
class MusicAdmin(ImportExportModelAdmin):
    list_display = ('id', 'author', 'title', 'read', 'total_like', 'comment_count', 'download', 'publish', 'created', 'updated')
    list_select_related = ('author',)
    search_fields = ('title', 'author__nickname', 'created')
    ordering = ('author', '-created')
    filter_horizontal = ('hashtag', 'like')
    readonly_fields = ('total_like', 'comment_count', 'created', 'updated')
    inlines = [CommentInlineAdmin]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('author', 'title', 'content', 'lyric', 'music', 'hashtag', 'like', 'read', 'publish', 'download')}),
        ('確認項目', {'fields': ('total_like', 'comment_count', 'created', 'updated')})
    ]


@admin.register(Comic)
class ComicAdmin(ImportExportModelAdmin):
    list_display = ('id', 'author', 'title', 'read', 'total_like', 'comment_count', 'publish', 'created', 'updated')
    list_select_related = ('author',)
    search_fields = ('title', 'author__nickname', 'created')
    ordering = ('author', '-created')
    filter_horizontal = ('hashtag', 'like')
    readonly_fields = ('total_like', 'comment_count', 'created', 'updated')
    inlines = [CommentInlineAdmin, ComicPageInlineAdmin]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('author', 'title', 'content', 'image', 'hashtag', 'like', 'read', 'publish')}),
        ('確認項目', {'fields': ('total_like', 'comment_count', 'created', 'updated')})
    ]


@admin.register(Picture)
class PictureAdmin(ImportExportModelAdmin):
    list_display = ('id', 'author', 'title', 'read', 'total_like', 'comment_count', 'publish', 'created', 'updated')
    list_select_related = ('author',)
    search_fields = ('title', 'author__nickname', 'created')
    ordering = ('author', '-created')
    filter_horizontal = ('hashtag', 'like')
    readonly_fields = ('total_like', 'comment_count', 'created', 'updated')
    inlines = [CommentInlineAdmin]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('author', 'title', 'content', 'image', 'hashtag', 'like', 'read', 'publish')}),
        ('確認項目', {'fields': ('total_like', 'comment_count', 'created', 'updated')})
    ]


@admin.register(Blog)
class BlogAdmin(ImportExportModelAdmin):
    list_display = ('id', 'author', 'title', 'read', 'total_like', 'comment_count', 'publish', 'created', 'updated')
    list_select_related = ('author',)
    search_fields = ('title', 'author__nickname', 'created')
    ordering = ('author', '-created')
    filter_horizontal = ('hashtag', 'like')
    readonly_fields = ('total_like', 'comment_count', 'created', 'updated')
    inlines = [CommentInlineAdmin]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('author', 'title', 'content', 'delta', 'image', 'hashtag', 'like', 'read', 'publish')}),
        ('確認項目', {'fields': ('total_like', 'comment_count', 'created', 'updated')})
    ]

    def save_model(self, request, obj, form, change):
        obj.richtext = json.loads(request.POST.dict()['delta'])['html']
        super(BlogAdmin, self).save_model(request, obj, form, change)


@admin.register(Chat)
class ChatAdmin(ImportExportModelAdmin):
    list_display = ('id', 'author', 'title', 'read', 'total_like', 'thread_count', 'joined_count', 'period', 'publish', 'created', 'updated')
    list_select_related = ('author',)
    search_fields = ('title', 'author__nickname', 'created')
    ordering = ('author', '-created')
    filter_horizontal = ('hashtag', 'like')
    readonly_fields = ('total_like', 'thread_count', 'joined_count', 'created', 'updated')
    inlines = [MessageInlineAdmin]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('author', 'title', 'content', 'hashtag', 'like', 'read', 'period', 'publish')}),
        ('確認項目', {'fields': ('total_like', 'thread_count', 'joined_count', 'created', 'updated')})
    ]


@admin.register(Todo)
class TodoAdmin(ImportExportModelAdmin):
    list_display = ('id', 'author', 'title', 'comment_count', 'priority', 'progress', 'duedate')
    list_select_related = ('author',)
    list_filter = ('priority', 'progress', 'duedate')
    search_fields = ('title', 'author__nickname', 'priority', 'progress', 'duedate')
    ordering = ('author', 'priority', '-duedate')
    readonly_fields = ('comment_count', 'created', 'updated')
    inlines = [CommentInlineAdmin]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('author', 'title', 'content', 'priority', 'progress', 'duedate')}),
        ('確認項目', {'fields': ('comment_count', 'created', 'updated')})
    ]


@admin.register(Follow)
class FollowAdmin(ImportExportModelAdmin):
    list_display = ('id', 'follower', 'following', 'created')
    list_select_related = ('follower', 'following')
    search_fields = ('follower__nickname', 'following__nickname', 'created')
    ordering = ('follower', 'following', '-created')
    readonly_fields = ('created',)

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('follower', 'following')}),
        ('確認項目', {'fields': ('created',)})
    ]


@admin.register(Notification)
class NotificationAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user_from', 'user_to', 'type_no', 'type_name', 'content_type', 'object_id', 'title', 'confirmed_count', 'deleted_count', 'created')
    list_select_related = ('user_from', 'user_to', 'content_type')
    search_fields = ('type_name', 'created')
    ordering = ('type_no', 'created')
    filter_horizontal = ('confirmed', 'deleted')
    readonly_fields = ('title', 'confirmed_count', 'deleted_count', 'created')

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('user_from', 'user_to', 'type_no', 'type_name', 'content_type', 'object_id', 'confirmed', 'deleted')}),
        ('確認項目', {'fields': ('title', 'confirmed_count', 'deleted_count', 'created')})
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('confirmed', 'deleted', 'content_object')


@admin.register(Advertise)
class AdvertiseAdmin(ImportExportModelAdmin):
    list_display = ('id', 'author', 'title', 'url', 'read', 'type', 'period', 'publish', 'created', 'updated')
    list_select_related = ('author',)
    search_fields = ('title', 'author__nickname', 'created')
    ordering = ('author', 'created')
    readonly_fields = ('read', 'created', 'updated')

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('author', 'title', 'url', 'content', 'image', 'video', 'type', 'period', 'publish')}),
        ('確認項目', {'fields': ('read', 'created', 'updated')})
    ]


@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin):
    list_display = ('id', 'content_type', 'object_id', 'author', 'parent', 'text', 'total_like', 'reply_count', 'created', 'updated')
    list_select_related = ('author', 'parent')
    search_fields = ('text', 'author__nickname', 'created', 'updated')
    ordering = ('created',)
    filter_horizontal = ('like',)
    readonly_fields = ('total_like', 'reply_count', 'created', 'updated')

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('author', 'parent', 'text', 'like', 'content_type', 'object_id')}),
        ('確認項目', {'fields': ('total_like', 'reply_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(reply_count=Count('reply')).select_related('content_type')


@admin.register(Message)
class MessageAdmin(ImportExportModelAdmin):
    list_display = ('id', 'author', 'chat', 'parent', 'text', 'reply_count', 'created', 'updated')
    list_select_related = ('author', 'chat', 'parent')
    search_fields = ('text', 'author__nickname', 'created', 'updated')
    ordering = ('created',)
    readonly_fields = ('reply_count', 'created', 'updated')

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('author', 'chat', 'parent', 'content')}),
        ('確認項目', {'fields': ('reply_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(reply_count=Count('reply'))


# MyPgage用の管理画面
class MyUsAdminSite(AdminSite):
    site_title = 'MyUs投稿管理'
    site_header = 'MyUs投稿管理'
    index_title = 'メニュー'
    index_template = ''
    site_url = '/'

    login_form = AuthenticationForm

    def has_permission(self, request):
        return request.user.is_active

manage_site = MyUsAdminSite(name='mymanage')
manage_site.disable_action('delete_selected')


class CommentInline(GenericTabularInline):
    model = Comment
    extra = 0
    max_num = 100
    exclude = ('like', 'reply_count')
    readonly_fields = ('author', 'parent', 'text', 'total_like')
    verbose_name_plural = 'コメント'

    def has_add_permission(self, request, obj=None):
        return False

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'いいね数'


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    max_num = 100
    exclude = ('content', 'reply_count')
    readonly_fields = ('author', 'parent', 'text')
    verbose_name_plural = 'メッセージ'

    def has_add_permission(self, request, obj=None):
        return False


class ComicPageInline(admin.StackedInline):
    model = ComicPage
    extra = 0
    max_num = 200
    verbose_name_plural = 'コミックページ情報'

    def has_delete_permission(self, request, obj=None):
        return False


class SearchTagAdminSite(admin.ModelAdmin):
    list_display = ('id', 'sequence', 'name', 'created')
    list_editable = ('sequence', 'name')
    list_per_page = 20
    search_fields = ('name', 'created')
    ordering = ('sequence', 'created')
    actions = ('delete_action',)
    readonly_fields = ('created',)

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('sequence', 'name')}),
        ('確認項目', {'fields': ('created',)})
    ]

    def get_queryset(self, request):
        qs = super(SearchTagAdminSite, self).get_queryset(request)
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(SearchTagAdminSite, self).save_model(request, obj, form, change)

    def delete_action(self, request, queryset):
        queryset.delete()
    delete_action.short_description = '削除する'
manage_site.register(SearchTag, SearchTagAdminSite)


class HashTagAdminSite(admin.ModelAdmin):
    list_display = ('id', 'jp_name', 'en_name')
    search_fields = ('jp_name', 'en_name')
    ordering = ('id',)

    # 詳細画面
    fieldsets = [
        ('確認項目', {'fields': ('jp_name', 'en_name')}),
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
manage_site.register(HashTag, HashTagAdminSite)


class PublishMixin:
    def published(self, request, queryset):
        queryset.update(publish=True)
    published.short_description = '公開する'

    def unpublished(self, request, queryset):
        queryset.update(publish=False)
    unpublished.short_description = '非公開にする'


class VideoAdminSite(admin.ModelAdmin, PublishMixin):
    list_display = ('id', 'title', 'read', 'total_like', 'comment_count', 'publish', 'created', 'updated')
    list_editable = ('title',)
    search_fields = ('title', 'created')
    ordering = ('-created',)
    actions = ('published', 'unpublished')
    filter_horizontal = ('hashtag',)
    readonly_fields = ('read', 'total_like', 'comment_count', 'created', 'updated')
    inlines = [CommentInline]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'image', 'video', 'convert', 'hashtag', 'publish')}),
        ('確認項目', {'fields': ('read', 'total_like', 'comment_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        qs = super(VideoAdminSite, self).get_queryset(request).prefetch_related('hashtag', 'like')
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(VideoAdminSite, self).save_model(request, obj, form, change)
manage_site.register(Video, VideoAdminSite)


class MusicAdminSite(admin.ModelAdmin, PublishMixin):
    list_display = ('id', 'title', 'read', 'total_like', 'comment_count', 'download', 'publish', 'created', 'updated')
    list_editable = ('title',)
    search_fields = ('title', 'created')
    ordering = ('-created',)
    actions = ('published', 'unpublished')
    filter_horizontal = ('hashtag',)
    readonly_fields = ('read', 'total_like', 'comment_count', 'created', 'updated')
    inlines = [CommentInline]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'lyric', 'music', 'hashtag', 'download', 'publish')}),
        ('確認項目', {'fields': ('read', 'total_like', 'comment_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        qs = super(MusicAdminSite, self).get_queryset(request).prefetch_related('hashtag', 'like')
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(MusicAdminSite, self).save_model(request, obj, form, change)
manage_site.register(Music, MusicAdminSite)


class ComicAdminSite(admin.ModelAdmin, PublishMixin):
    list_display = ('id', 'title', 'read', 'total_like', 'comment_count', 'publish', 'created', 'updated')
    list_editable = ('title',)
    search_fields = ('title', 'created')
    ordering = ('-created',)
    actions = ('published', 'unpublished')
    filter_horizontal = ('hashtag',)
    readonly_fields = ('read', 'total_like', 'comment_count', 'created', 'updated')
    inlines = [CommentInline, ComicPageInline]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'image', 'hashtag', 'publish')}),
        ('確認項目', {'fields': ('read', 'total_like', 'comment_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        qs = super(ComicAdminSite, self).get_queryset(request).prefetch_related('hashtag', 'like')
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(ComicAdminSite, self).save_model(request, obj, form, change)
manage_site.register(Comic, ComicAdminSite)


class PictureAdminSite(admin.ModelAdmin, PublishMixin):
    list_display = ('id', 'title', 'read', 'total_like', 'comment_count', 'publish', 'created', 'updated')
    list_editable = ('title',)
    search_fields = ('title', 'created')
    ordering = ('-created',)
    actions = ('published', 'unpublished')
    filter_horizontal = ('hashtag',)
    readonly_fields = ('read', 'total_like', 'comment_count', 'created', 'updated')
    inlines = [CommentInline]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'image', 'hashtag', 'publish')}),
        ('確認項目', {'fields': ('read', 'total_like', 'comment_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        qs = super(PictureAdminSite, self).get_queryset(request).prefetch_related('hashtag', 'like')
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(PictureAdminSite, self).save_model(request, obj, form, change)
manage_site.register(Picture, PictureAdminSite)


class BlogAdminSite(admin.ModelAdmin, PublishMixin):
    list_display = ('id', 'title', 'read', 'total_like', 'comment_count', 'publish', 'created', 'updated')
    list_editable = ('title',)
    search_fields = ('title', 'created')
    ordering = ('-created',)
    actions = ('published', 'unpublished')
    filter_horizontal = ('hashtag',)
    readonly_fields = ('read', 'total_like', 'comment_count', 'created', 'updated')
    inlines = [CommentInline]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'delta', 'image', 'hashtag', 'publish')}),
        ('確認項目', {'fields': ('read', 'total_like', 'comment_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        qs = super(BlogAdminSite, self).get_queryset(request).prefetch_related('hashtag', 'like')
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.richtext = json.loads(request.POST.dict()['delta'])['html']
        super(BlogAdminSite, self).save_model(request, obj, form, change)
manage_site.register(Blog, BlogAdminSite)


class ChatAdminSite(admin.ModelAdmin, PublishMixin):
    list_display = ('id', 'title', 'read', 'total_like', 'thread_count', 'joined_count', 'period', 'publish', 'created', 'updated')
    list_editable = ('title',)
    search_fields = ('title', 'created')
    ordering = ('-created',)
    actions = ('published', 'unpublished')
    filter_horizontal = ('hashtag',)
    readonly_fields = ('read', 'total_like', 'thread_count', 'joined_count', 'created', 'updated')
    inlines = [MessageInline]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'hashtag', 'period', 'publish')}),
        ('確認項目', {'fields': ('read', 'total_like', 'thread_count', 'joined_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        qs = super(ChatAdminSite, self).get_queryset(request).prefetch_related('hashtag', 'like')
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(ChatAdminSite, self).save_model(request, obj, form, change)
manage_site.register(Chat, ChatAdminSite)


class TodoAdminSite(admin.ModelAdmin):
    list_display = ('id', 'title', 'comment_count', 'priority', 'progress', 'duedate')
    list_editable = ('title', 'priority', 'progress', 'duedate')
    list_filter = ('priority', 'progress', 'duedate')
    search_fields = ('title', 'duedate')
    ordering = ('priority', '-duedate')
    actions = ('delete_action',)
    readonly_fields = ('comment_count', 'created', 'updated')
    inlines = [CommentInline]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'priority', 'progress', 'duedate')}),
        ('確認項目', {'fields': ('comment_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        qs = super(TodoAdminSite, self).get_queryset(request)
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(TodoAdminSite, self).save_model(request, obj, form, change)

    def delete_action(self, request, queryset):
        queryset.delete()
    delete_action.short_description = '削除する'
manage_site.register(Todo, TodoAdminSite)


class FollowAdminSite(admin.ModelAdmin):
    list_display = ('id', 'following', 'created')
    list_select_related = ('following',)
    search_fields = ('following__nickname', 'following__introduction', 'created')
    ordering = ('following', '-created')
    actions = ('delete_action',)
    readonly_fields = ('following', 'created')

    # 詳細画面
    fieldsets = [
        ('確認項目', {'fields': ('following', 'following_introduction', 'created')})
    ]

    def get_queryset(self, request):
        qs = super(FollowAdminSite, self).get_queryset(request)
        return qs.filter(follower=request.user)

    def save_model(self, request, obj, form, change):
        obj.follower = request.user
        super(FollowAdminSite, self).save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def delete_action(self, request, queryset):
        queryset.delete()
    delete_action.short_description = '削除する'

    def following_introduction(self, obj):
        return obj.following.introduction
    following_introduction.short_description = 'Introduction'
manage_site.register(Follow, FollowAdminSite)


class NotificationAdminSite(admin.ModelAdmin):
    list_display = ('id', 'type_no', 'type_name', 'title', 'confirmed_count', 'created')
    search_fields = ('type_name', 'created')
    ordering = ('type_no', 'created')
    filter_horizontal = ('confirmed', 'deleted')
    readonly_fields = ('type_no', 'type_name', 'title', 'confirmed_count', 'created')

    # 詳細画面
    fieldsets = [
        ('確認項目', {'fields': ('type_no', 'type_name', 'title', 'confirmed_count', 'created')}),
    ]

    def get_queryset(self, request):
        qs = super(NotificationAdminSite, self).get_queryset(request).prefetch_related('confirmed', 'deleted')
        return qs.filter(user_from=request.user).exclude(type_no__in=(8, 9, 10, 11))

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def confirmed_count(self, obj):
        return obj.confirmed.count()
    confirmed_count.short_description = 'confirmed'

    def title(self, obj):
        return obj.content_object
    title.short_description = 'title'
manage_site.register(Notification, NotificationAdminSite)


class AdvertiseAdminSite(admin.ModelAdmin, PublishMixin):
    list_display = ('id', 'title', 'url', 'read', 'period', 'publish', 'created', 'updated')
    list_select_related = ('author',)
    search_fields = ('title', 'created')
    ordering = ('author', 'created')
    actions = ('published', 'unpublished')
    readonly_fields = ('read', 'created', 'updated')

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'url', 'content', 'image', 'video', 'period', 'publish')}),
        ('確認項目', {'fields': ('read', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        qs = super(AdvertiseAdminSite, self).get_queryset(request)
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.type = 1
        super(AdvertiseAdminSite, self).save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return request.user.plan() != 'Free'

    def has_change_permission(self, request, obj=None):
        return request.user.plan() != 'Free'
manage_site.register(Advertise, AdvertiseAdminSite)
