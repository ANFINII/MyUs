from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.contenttypes.admin import GenericTabularInline
from import_export.admin import ImportExportModelAdmin
from .models import User, MyPage, SearchTag, HashTag, NotificationSetting, Notification, Comment, Follow
from .models import Video, Live, Music, Picture, Blog, Chat, Collabo, Todo, Advertise
import datetime

# Admin用の管理画面
class MyPageInline(admin.StackedInline):
    model = MyPage
    readonly_fields = ('banner', 'follow_num', 'follower_num', 'rate_plan', 'rate_plan_date', 'is_advertise')
    verbose_name = 'Myページ情報'

    def has_delete_permission(self, request, obj=None):
        return False

class NotificationSettingInline(admin.TabularInline):
    model = NotificationSetting
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
    fields = ('author', 'parent', 'text', 'total_like')
    readonly_fields = ('total_like',)
    verbose_name_plural = 'コメント'

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'いいね数'

@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    list_display = ('id', 'email', 'username', 'nickname', 'fullname', 'birthday', 'age', 'gender', 'rate_plan')
    list_filter = ('birthday', 'gender')
    search_fields = ('email', 'username', 'nickname', 'last_name', 'first_name', 'phone')
    ordering = ('id',)
    filter_horizontal = ('groups', 'user_permissions')
    readonly_fields = ('birthday', 'age', 'date_joined', 'last_login')
    inlines = [MyPageInline, NotificationSettingInline, SearchTagInline]

    # 詳細画面
    fieldsets = [
        ('アカウント情報', {'fields': ('image', 'email', 'username', 'nickname', 'last_name', 'first_name', 'birthday', 'age', 'gender', 'phone', 'location', 'introduction', 'groups', 'user_permissions')}),
        ('権限情報', {'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser', 'date_joined', 'last_login')}),
    ]

    def fullname(self, obj):
        return obj.last_name + ' ' + obj.first_name
    fullname.short_description = 'fullname'

    def age(self, obj):
        if obj.birthday is not None:
            DAYS_IN_YEAR = 365.2425
            return int((datetime.date.today() - obj.birthday).days / DAYS_IN_YEAR)
    age.short_description = 'age'

    def rate_plan(self, obj):
        RATE_PLAN = {'0': 'Free', '1': 'Basic', '2': 'Standard', '3': 'Premium'}
        mypage_obj = MyPage.objects.values_list('rate_plan').get(user_id=obj.id)
        for rate_plan in mypage_obj:
            for rate_paln_key, rate_paln_value in RATE_PLAN.items():
                if rate_plan in rate_paln_key:
                    return rate_paln_value
    rate_plan.short_description = 'rate plan'

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
    list_display = ('id', 'author', 'title', 'read', 'total_like', 'comment_count', 'publish', 'created', 'updated')
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

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('hashtag', 'like')

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'

    def comment_count(self, obj):
        return obj.comment.all().count()
    comment_count.short_description = 'comment'

@admin.register(Live)
class LiveAdmin(ImportExportModelAdmin):
    list_display = ('id', 'author', 'title', 'read', 'total_like', 'comment_count', 'publish', 'created', 'updated')
    list_select_related = ('author',)
    search_fields = ('title', 'author__nickname', 'created')
    ordering = ('author', '-created')
    filter_horizontal = ('hashtag', 'like')
    readonly_fields = ('total_like', 'comment_count', 'created', 'updated')
    inlines = [CommentInlineAdmin]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('author', 'title', 'content', 'image', 'live', 'hashtag', 'like', 'read', 'publish')}),
        ('確認項目', {'fields': ('total_like', 'comment_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('hashtag', 'like')

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'

    def comment_count(self, obj):
        return obj.comment.all().count()
    comment_count.short_description = 'comment'

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

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('hashtag', 'like')

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'

    def comment_count(self, obj):
        return obj.comment.all().count()
    comment_count.short_description = 'comment'

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

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('hashtag', 'like')

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'

    def comment_count(self, obj):
        return obj.comment.all().count()
    comment_count.short_description = 'comment'

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
        ('編集項目', {'fields': ('author', 'title', 'content', 'image', 'richtext', 'hashtag', 'like', 'read', 'publish')}),
        ('確認項目', {'fields': ('total_like', 'comment_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('hashtag', 'like')

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'

    def comment_count(self, obj):
        return obj.comment.all().count()
    comment_count.short_description = 'comment'

@admin.register(Chat)
class ChatAdmin(ImportExportModelAdmin):
    list_display = ('id', 'author', 'title', 'read', 'total_like', 'comment_count', 'user_count', 'period', 'publish', 'created', 'updated')
    list_select_related = ('author',)
    search_fields = ('title', 'author__nickname', 'created')
    ordering = ('author', '-created')
    filter_horizontal = ('hashtag', 'like')
    readonly_fields = ('total_like', 'comment_count', 'user_count', 'created', 'updated')
    inlines = [CommentInlineAdmin]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('author', 'title', 'content', 'hashtag', 'like', 'read', 'period', 'publish')}),
        ('確認項目', {'fields': ('total_like', 'comment_count', 'user_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('hashtag', 'like')

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'

    def comment_count(self, obj):
        return obj.comment.filter(parent__isnull=True).count()
    comment_count.short_description = 'thread'

    def user_count(self, obj):
        return obj.comment.order_by('author').distinct().values_list('author').count()
    user_count.short_description = 'joined'

@admin.register(Collabo)
class CollaboAdmin(ImportExportModelAdmin):
    list_display = ('id', 'author', 'title', 'read', 'total_like', 'comment_count', 'period', 'publish', 'created', 'updated')
    list_select_related = ('author',)
    search_fields = ('title', 'author__nickname', 'created')
    ordering = ('author', '-created')
    filter_horizontal = ('hashtag', 'like')
    readonly_fields = ('total_like', 'comment_count', 'created', 'updated')
    inlines = [CommentInlineAdmin]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('author', 'title', 'content', 'hashtag', 'like', 'read', 'period', 'publish')}),
        ('確認項目', {'fields': ('total_like', 'comment_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('hashtag', 'like')

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'

    def comment_count(self, obj):
        return obj.comment.all().count()
    comment_count.short_description = 'comment'

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

    def comment_count(self, obj):
        return obj.comment.all().count()
    comment_count.short_description = 'comment'

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
        return super().get_queryset(request).prefetch_related('confirmed', 'deleted')

    def confirmed_count(self, obj):
        return obj.confirmed.count()
    confirmed_count.short_description = 'confirmed'

    def deleted_count(self, obj):
        return obj.deleted.count()
    deleted_count.short_description = 'deleted'

    def title(self, obj):
        return obj.content_object
    title.short_description = 'title'

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
    list_display = ('id', 'content_type', 'object_id', 'content_object', 'author', 'text', 'parent_id', 'total_like', 'created', 'updated')
    list_select_related = ('author', 'parent', 'content_type')
    search_fields = ('text', 'author__nickname', 'created', 'updated')
    ordering = ('content_type', 'object_id', 'id')
    filter_horizontal = ('like',)
    readonly_fields = ('total_like', 'created', 'updated')

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('author', 'parent', 'text', 'like', 'content_type', 'object_id')}),
        ('確認項目', {'fields': ('total_like', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('like')

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'


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

mymanage_site = MyUsAdminSite(name='mymanage')
mymanage_site.disable_action('delete_selected')

class CommentInline(GenericTabularInline):
    model = Comment
    extra = 0
    max_num = 100
    exclude = ('like',)
    readonly_fields = ('author', 'parent', 'text', 'total_like')
    verbose_name_plural = 'コメント'

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'いいね数'

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
mymanage_site.register(SearchTag, SearchTagAdminSite)

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
mymanage_site.register(HashTag, HashTagAdminSite)

class VideoAdminSite(admin.ModelAdmin):
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

    def published(self, request, queryset):
        queryset.update(publish=True)
    published.short_description = '公開する'

    def unpublished(self, request, queryset):
        queryset.update(publish=False)
    unpublished.short_description = '非公開にする'

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'

    def comment_count(self, obj):
        return obj.comment.all().count()
    comment_count.short_description = 'comment'
mymanage_site.register(Video, VideoAdminSite)

class LiveAdminSite(admin.ModelAdmin):
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
        ('編集項目', {'fields': ('title', 'content', 'image', 'live', 'hashtag', 'publish')}),
        ('確認項目', {'fields': ('read', 'total_like', 'comment_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        qs = super(LiveAdminSite, self).get_queryset(request).prefetch_related('hashtag', 'like')
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(LiveAdminSite, self).save_model(request, obj, form, change)

    def published(self, request, queryset):
        queryset.update(publish=True)
    published.short_description = '公開する'

    def unpublished(self, request, queryset):
        queryset.update(publish=False)
    unpublished.short_description = '非公開にする'

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'

    def comment_count(self, obj):
        return obj.comment.all().count()
    comment_count.short_description = 'comment'
mymanage_site.register(Live, LiveAdminSite)

class MusicAdminSite(admin.ModelAdmin):
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

    def published(self, request, queryset):
        queryset.update(publish=True)
    published.short_description = '公開する'

    def unpublished(self, request, queryset):
        queryset.update(publish=False)
    unpublished.short_description = '非公開にする'

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'

    def comment_count(self, obj):
        return obj.comment.all().count()
    comment_count.short_description = 'comment'
mymanage_site.register(Music, MusicAdminSite)

class PictureAdminSite(admin.ModelAdmin):
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

    def published(self, request, queryset):
        queryset.update(publish=True)
    published.short_description = '公開する'

    def unpublished(self, request, queryset):
        queryset.update(publish=False)
    unpublished.short_description = '非公開にする'

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'

    def comment_count(self, obj):
        return obj.comment.all().count()
    comment_count.short_description = 'comment'
mymanage_site.register(Picture, PictureAdminSite)

class BlogAdminSite(admin.ModelAdmin):
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
        ('編集項目', {'fields': ('title', 'content', 'image', 'richtext', 'hashtag', 'publish')}),
        ('確認項目', {'fields': ('read', 'total_like', 'comment_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        qs = super(BlogAdminSite, self).get_queryset(request).prefetch_related('hashtag', 'like')
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(BlogAdminSite, self).save_model(request, obj, form, change)

    def published(self, request, queryset):
        queryset.update(publish=True)
    published.short_description = '公開する'

    def unpublished(self, request, queryset):
        queryset.update(publish=False)
    unpublished.short_description = '非公開にする'

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'

    def comment_count(self, obj):
        return obj.comment.all().count()
    comment_count.short_description = 'comment'
mymanage_site.register(Blog, BlogAdminSite)

class ChatAdminSite(admin.ModelAdmin):
    list_display = ('id', 'title', 'read', 'total_like', 'comment_count', 'user_count', 'period', 'publish', 'created', 'updated')
    list_editable = ('title',)
    search_fields = ('title', 'created')
    ordering = ('-created',)
    actions = ('published', 'unpublished')
    filter_horizontal = ('hashtag',)
    readonly_fields = ('read', 'total_like', 'comment_count', 'user_count', 'created', 'updated')
    inlines = [CommentInline]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'hashtag', 'period', 'publish')}),
        ('確認項目', {'fields': ('read', 'total_like', 'comment_count', 'user_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        qs = super(ChatAdminSite, self).get_queryset(request).prefetch_related('hashtag', 'like')
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(ChatAdminSite, self).save_model(request, obj, form, change)

    def published(self, request, queryset):
        queryset.update(publish=True)
    published.short_description = '公開する'

    def unpublished(self, request, queryset):
        queryset.update(publish=False)
    unpublished.short_description = '非公開にする'

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'

    def comment_count(self, obj):
        return obj.comment.filter(parent__isnull=True).count()
    comment_count.short_description = 'thread'

    def user_count(self, obj):
        return obj.comment.order_by('author').distinct().values_list('author').count()
    user_count.short_description = 'joined'
mymanage_site.register(Chat, ChatAdminSite)

class CollaboAdminSite(admin.ModelAdmin):
    list_display = ('id', 'title', 'read', 'total_like', 'comment_count', 'period', 'publish', 'created', 'updated')
    list_editable = ('title',)
    search_fields = ('title', 'created')
    ordering = ('-created',)
    actions = ('published', 'unpublished')
    filter_horizontal = ('hashtag',)
    readonly_fields = ('read', 'total_like', 'comment_count', 'created', 'updated')
    inlines = [CommentInline]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'hashtag', 'period', 'publish')}),
        ('確認項目', {'fields': ('read', 'total_like', 'comment_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        qs = super(CollaboAdminSite, self).get_queryset(request).prefetch_related('hashtag', 'like')
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(CollaboAdminSite, self).save_model(request, obj, form, change)

    def published(self, request, queryset):
        queryset.update(publish=True)
    published.short_description = '公開する'

    def unpublished(self, request, queryset):
        queryset.update(publish=False)
    unpublished.short_description = '非公開にする'

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'

    def comment_count(self, obj):
        return obj.comment.all().count()
    comment_count.short_description = 'comment'
mymanage_site.register(Collabo, CollaboAdminSite)

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

    def comment_count(self, obj):
        return obj.comment.all().count()
    comment_count.short_description = 'comment'
mymanage_site.register(Todo, TodoAdminSite)

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
mymanage_site.register(Follow, FollowAdminSite)

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
mymanage_site.register(Notification, NotificationAdminSite)

class AdvertiseAdminSite(admin.ModelAdmin):
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
        author = request.user
        if author.mypage.rate_plan != '0':
            return True
        return False

    def has_change_permission(self, request, obj=None):
        author = request.user
        if author.mypage.rate_plan != '0':
            return True
        return False

    def published(self, request, queryset):
        queryset.update(publish=True)
    published.short_description = '公開する'

    def unpublished(self, request, queryset):
        queryset.update(publish=False)
    unpublished.short_description = '非公開にする'
mymanage_site.register(Advertise, AdvertiseAdminSite)
