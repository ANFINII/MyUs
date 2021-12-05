from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.contenttypes.admin import GenericTabularInline
from import_export.admin import ImportExportModelAdmin
from .models import User, SearchTagModel, TagModel, NotificationModel, CommentModel, FollowModel, AdvertiseModel
from .models import VideoModel, LiveModel, MusicModel, PictureModel, BlogModel, ChatModel, CollaboModel, TodoModel

# Admin用の管理画面
class SearchTagInline(admin.TabularInline):
    model = SearchTagModel
    extra = 1
    max_num = 20
    verbose_name_plural = '検索タグ'

class CommentInlineAdmin(GenericTabularInline):
    model = CommentModel
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
    list_display = ('id', 'username', 'email', 'nickname', 'full_name', 'birthday', 'age', 'gender', 'phone', 'following_count', 'follower_count')
    list_filter = ('birthday', 'gender')
    search_fields = ('username', 'email', 'nickname', 'full_name', 'phone')
    ordering = ('id',)
    filter_horizontal = ('groups', 'user_permissions')
    readonly_fields = ('full_name', 'birthday', 'age', 'date_joined', 'last_login', 'following_count', 'follower_count')
    inlines = [SearchTagInline]

    # 詳細画面
    fieldsets = [
        ('アカウント情報', {'fields': ('user_image', 'username', 'email', 'nickname', 'full_name', 'birthday', 'age', 'gender', 'phone', 'location', 'profession', 'introduction', 'groups', 'user_permissions')}),
        ('権限情報', {'fields': ('is_active', 'is_premium', 'is_staff', 'is_admin', 'is_superuser', 'date_joined', 'last_login')}),
        ('Myページ情報', {'fields': ('mypage_image', 'mypage_email', 'content', 'following_count', 'follower_count')})
    ]

@admin.register(SearchTagModel)
class SearchTagAdmin(ImportExportModelAdmin):
    list_display = ('id', 'author', 'sequence', 'searchtag', 'created')
    list_select_related = ('author',)
    list_per_page = 20
    search_fields = ('author__nickname', 'searchtag', 'created')
    ordering = ('author', 'sequence', 'created')
    readonly_fields = ('author', 'created')

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('sequence', 'searchtag')}),
        ('確認項目', {'fields': ('author', 'created')})
    ]

@admin.register(TagModel)
class TagAdmin(ImportExportModelAdmin):
    list_display = ('id', 'tag', 'english_tag')
    list_editable = ('tag', 'english_tag')
    search_fields = ('tag', 'english_tag')
    ordering = ('id',)

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('tag', 'english_tag')}),
    ]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(TagAdmin, self).save_model(request, obj, form, change)

@admin.register(VideoModel)
class VideoModelAdmin(ImportExportModelAdmin):
    list_display = ('id', 'author', 'title', 'publish', 'read', 'total_like', 'comment_count', 'created', 'updated')
    list_select_related = ('author',)
    search_fields = ('title', 'author__nickname', 'created')
    ordering = ('author', '-created')
    filter_horizontal = ('tags', 'like')
    readonly_fields = ('total_like', 'comment_count', 'created', 'updated')
    inlines = [CommentInlineAdmin]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('author', 'title', 'content', 'images', 'videos', 'publish', 'tags', 'like', 'read')}),
        ('確認項目', {'fields': ('total_like', 'comment_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags', 'like')

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'

    def comment_count(self, obj):
        return obj.comments.all().count()
    comment_count.short_description = 'comment'

@admin.register(LiveModel)
class LiveModelAdmin(ImportExportModelAdmin):
    list_display = ('id', 'author', 'title', 'publish', 'read', 'total_like', 'comment_count', 'created', 'updated')
    list_select_related = ('author',)
    search_fields = ('title', 'author__nickname', 'created')
    ordering = ('author', '-created')
    filter_horizontal = ('tags', 'like')
    readonly_fields = ('total_like', 'comment_count', 'created', 'updated')
    inlines = [CommentInlineAdmin]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('author', 'title', 'content', 'images', 'lives', 'publish', 'tags', 'like', 'read')}),
        ('確認項目', {'fields': ('total_like', 'comment_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags', 'like')

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'

    def comment_count(self, obj):
        return obj.comments.all().count()
    comment_count.short_description = 'comment'

@admin.register(MusicModel)
class MusicModelAdmin(ImportExportModelAdmin):
    list_display = ('id', 'author', 'title', 'publish', 'read', 'total_like', 'comment_count', 'created', 'updated')
    list_select_related = ('author',)
    search_fields = ('title', 'author__nickname', 'created')
    ordering = ('author', '-created')
    filter_horizontal = ('tags', 'like')
    readonly_fields = ('total_like', 'comment_count', 'created', 'updated')
    inlines = [CommentInlineAdmin]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('author', 'title', 'content', 'lyrics', 'musics', 'publish', 'tags', 'like', 'read')}),
        ('確認項目', {'fields': ('total_like', 'comment_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags', 'like')

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'

    def comment_count(self, obj):
        return obj.comments.all().count()
    comment_count.short_description = 'comment'

@admin.register(PictureModel)
class PictureModelAdmin(ImportExportModelAdmin):
    list_display = ('id', 'author', 'title', 'publish', 'read', 'total_like', 'comment_count', 'created', 'updated')
    list_select_related = ('author',)
    search_fields = ('title', 'author__nickname', 'created')
    ordering = ('author', '-created')
    filter_horizontal = ('tags', 'like')
    readonly_fields = ('total_like', 'comment_count', 'created', 'updated')
    inlines = [CommentInlineAdmin]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('author', 'title', 'content', 'images', 'publish', 'tags', 'like', 'read')}),
        ('確認項目', {'fields': ('total_like', 'comment_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags', 'like')

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'

    def comment_count(self, obj):
        return obj.comments.all().count()
    comment_count.short_description = 'comment'

@admin.register(BlogModel)
class BlogModelAdmin(ImportExportModelAdmin):
    list_display = ('id', 'author', 'title', 'publish', 'read', 'total_like', 'comment_count', 'created', 'updated')
    list_select_related = ('author',)
    search_fields = ('title', 'author__nickname', 'created')
    ordering = ('author', '-created')
    filter_horizontal = ('tags', 'like')
    readonly_fields = ('total_like', 'comment_count', 'created', 'updated')
    inlines = [CommentInlineAdmin]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('author', 'title', 'content', 'images', 'richtext', 'publish', 'tags', 'like', 'read')}),
        ('確認項目', {'fields': ('total_like', 'comment_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags', 'like')

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'

    def comment_count(self, obj):
        return obj.comments.all().count()
    comment_count.short_description = 'comment'

@admin.register(ChatModel)
class ChatModelAdmin(ImportExportModelAdmin):
    list_display = ('id', 'author', 'title', 'publish', 'read', 'total_like', 'comment_count', 'user_count', 'period', 'created', 'updated')
    list_select_related = ('author',)
    search_fields = ('title', 'author__nickname', 'created')
    ordering = ('author', '-created')
    filter_horizontal = ('tags', 'like')
    readonly_fields = ('total_like', 'comment_count', 'user_count', 'created', 'updated')
    inlines = [CommentInlineAdmin]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('author', 'title', 'content', 'publish', 'tags', 'like', 'read', 'period')}),
        ('確認項目', {'fields': ('total_like', 'comment_count', 'user_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags', 'like')

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'

    def comment_count(self, obj):
        return obj.comments.filter(parent__isnull=True).count()
    comment_count.short_description = 'thread'

    def user_count(self, obj):
        return obj.comments.order_by('author').distinct().values_list('author').count()
    user_count.short_description = 'joined'

@admin.register(CollaboModel)
class CollaboModelAdmin(ImportExportModelAdmin):
    list_display = ('id', 'author', 'title', 'publish', 'read', 'total_like', 'comment_count', 'period', 'created', 'updated')
    list_select_related = ('author',)
    search_fields = ('title', 'author__nickname', 'created')
    ordering = ('author', '-created')
    filter_horizontal = ('tags', 'like')
    readonly_fields = ('total_like', 'comment_count', 'created', 'updated')
    inlines = [CommentInlineAdmin]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('author', 'title', 'content', 'publish', 'tags', 'like', 'read', 'period')}),
        ('確認項目', {'fields': ('total_like', 'comment_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags', 'like')

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'

    def comment_count(self, obj):
        return obj.comments.all().count()
    comment_count.short_description = 'comment'

@admin.register(TodoModel)
class TodoModelAdmin(ImportExportModelAdmin):
    list_display = ('id', 'author', 'title', 'comment_count', 'priority', 'duedate')
    list_select_related = ('author',)
    list_filter = ('priority', 'duedate')
    search_fields = ('title', 'author__nickname', 'priority', 'duedate')
    ordering = ('author', 'priority', '-duedate')
    readonly_fields = ('comment_count', 'created', 'updated')
    inlines = [CommentInlineAdmin]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('author', 'title', 'content', 'priority', 'duedate')}),
        ('確認項目', {'fields': ('comment_count', 'created', 'updated')})
    ]

    def comment_count(self, obj):
        return obj.comments.all().count()
    comment_count.short_description = 'comment'

@admin.register(FollowModel)
class FollowModelAdmin(ImportExportModelAdmin):
    list_display = ('id', 'follower', 'following', 'created')
    list_select_related = ('follower', 'following')
    search_fields = ('follower__nickname', 'following__nickname', 'created')
    ordering = ('follower', 'following', '-created')
    readonly_fields = ('created',)

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('follower', 'following',)}),
        ('確認項目', {'fields': ('created',)})
    ]

@admin.register(NotificationModel)
class NotificationAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user_from', 'user_to', 'type_no', 'content_type', 'object_id', 'title', 'confirmed_count', 'delete_count', 'created')
    search_fields = ('type_no', 'created')
    ordering = ('type_no', '-created')
    filter_horizontal = ('confirmed', 'delete')
    readonly_fields = ('title', 'confirmed_count', 'delete_count', 'created')

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('user_from', 'user_to', 'type_no', 'content_type', 'object_id', 'confirmed', 'delete')}),
        ('確認項目', {'fields': ('title', 'confirmed_count', 'delete_count', 'created')})
    ]

    def confirmed_count(self, obj):
        return obj.confirmed.count()
    confirmed_count.short_description = 'confirmed'

    def delete_count(self, obj):
        return obj.delete.count()
    delete_count.short_description = 'delete'

    def title(self, obj):
        return obj.content_object.title
    title.short_description = 'title'

@admin.register(AdvertiseModel)
class AdvertiseModelAdmin(ImportExportModelAdmin):
    list_display = ('id', 'author', 'title', 'url', 'publish', 'read', 'type', 'period', 'created', 'updated')
    list_select_related = ('author',)
    search_fields = ('title', 'author__nickname', 'created')
    ordering = ('author', 'created')
    readonly_fields = ('read', 'created', 'updated')

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('author', 'title', 'url', 'content', 'images', 'videos', 'publish', 'type', 'period')}),
        ('確認項目', {'fields': ('read', 'created', 'updated')})
    ]

@admin.register(CommentModel)
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
    model = CommentModel
    extra = 0
    max_num = 100
    exclude = ('like',)
    readonly_fields = ('author', 'parent', 'text', 'total_like')
    verbose_name_plural = 'コメント'

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'いいね数'

class SearchTagAdminSite(admin.ModelAdmin):
    list_display = ('id', 'sequence', 'searchtag', 'created')
    list_editable = ('sequence', 'searchtag',)
    list_per_page = 20
    search_fields = ('searchtag', 'created')
    ordering = ('sequence', 'created')
    actions = ('delete_action',)
    readonly_fields = ('created',)

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('sequence', 'searchtag')}),
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
mymanage_site.register(SearchTagModel, SearchTagAdminSite)

class TagAdminSite(admin.ModelAdmin):
    list_display = ('id', 'tag', 'english_tag')
    search_fields = ('tag', 'english_tag')
    ordering = ('id',)

    # 詳細画面
    fieldsets = [
        ('確認項目', {'fields': ('tag', 'english_tag')}),
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
mymanage_site.register(TagModel, TagAdminSite)

class VideoModelAdminSite(admin.ModelAdmin):
    list_display = ('id', 'title', 'publish', 'read', 'total_like', 'comment_count', 'created', 'updated')
    list_editable = ('title',)
    search_fields = ('title', 'created')
    ordering = ('-created',)
    actions = ('published', 'unpublished')
    filter_horizontal = ('tags',)
    readonly_fields = ('read', 'total_like', 'comment_count', 'created', 'updated')
    inlines = [CommentInline]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'images', 'videos', 'publish', 'tags')}),
        ('確認項目', {'fields': ('read', 'total_like', 'comment_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        qs = super(VideoModelAdminSite, self).get_queryset(request).prefetch_related('tags', 'like')
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(VideoModelAdminSite, self).save_model(request, obj, form, change)

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
        return obj.comments.all().count()
    comment_count.short_description = 'comment'
mymanage_site.register(VideoModel, VideoModelAdminSite)

class LiveModelAdminSite(admin.ModelAdmin):
    list_display = ('id', 'title', 'publish', 'read', 'total_like', 'comment_count', 'created', 'updated')
    list_editable = ('title',)
    search_fields = ('title', 'created')
    ordering = ('-created',)
    actions = ('published', 'unpublished')
    filter_horizontal = ('tags',)
    readonly_fields = ('read', 'total_like', 'comment_count', 'created', 'updated')
    inlines = [CommentInline]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'images', 'lives', 'publish', 'tags')}),
        ('確認項目', {'fields': ('read', 'total_like', 'comment_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        qs = super(LiveModelAdminSite, self).get_queryset(request).prefetch_related('tags', 'like')
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(LiveModelAdminSite, self).save_model(request, obj, form, change)

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
        return obj.comments.all().count()
    comment_count.short_description = 'comment'
mymanage_site.register(LiveModel, LiveModelAdminSite)

class MusicModelAdminSite(admin.ModelAdmin):
    list_display = ('id', 'title', 'publish', 'read', 'total_like', 'comment_count', 'created', 'updated')
    list_editable = ('title',)
    search_fields = ('title', 'created')
    ordering = ('-created',)
    actions = ('published', 'unpublished')
    filter_horizontal = ('tags',)
    readonly_fields = ('read', 'total_like', 'comment_count', 'created', 'updated')
    inlines = [CommentInline]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'lyrics', 'musics', 'publish', 'tags')}),
        ('確認項目', {'fields': ('read', 'total_like', 'comment_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        qs = super(MusicModelAdminSite, self).get_queryset(request).prefetch_related('tags', 'like')
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(MusicModelAdminSite, self).save_model(request, obj, form, change)

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
        return obj.comments.all().count()
    comment_count.short_description = 'comment'
mymanage_site.register(MusicModel, MusicModelAdminSite)

class PictureModelAdminSite(admin.ModelAdmin):
    list_display = ('id', 'title', 'publish', 'read', 'total_like', 'comment_count', 'created', 'updated')
    list_editable = ('title',)
    search_fields = ('title', 'created')
    ordering = ('-created',)
    actions = ('published', 'unpublished')
    filter_horizontal = ('tags',)
    readonly_fields = ('read', 'total_like', 'comment_count', 'created', 'updated')
    inlines = [CommentInline]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'images', 'publish', 'tags')}),
        ('確認項目', {'fields': ('read', 'total_like', 'comment_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        qs = super(PictureModelAdminSite, self).get_queryset(request).prefetch_related('tags', 'like')
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(PictureModelAdminSite, self).save_model(request, obj, form, change)

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
        return obj.comments.all().count()
    comment_count.short_description = 'comment'
mymanage_site.register(PictureModel, PictureModelAdminSite)

class BlogModelAdminSite(admin.ModelAdmin):
    list_display = ('id', 'title', 'publish', 'read', 'total_like', 'comment_count', 'created', 'updated')
    list_editable = ('title',)
    search_fields = ('title', 'created')
    ordering = ('-created',)
    actions = ('published', 'unpublished')
    filter_horizontal = ('tags',)
    readonly_fields = ('read', 'total_like', 'comment_count', 'created', 'updated')
    inlines = [CommentInline]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'images', 'richtext', 'publish', 'tags')}),
        ('確認項目', {'fields': ('read', 'total_like', 'comment_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        qs = super(BlogModelAdminSite, self).get_queryset(request).prefetch_related('tags', 'like')
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(BlogModelAdminSite, self).save_model(request, obj, form, change)

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
        return obj.comments.all().count()
    comment_count.short_description = 'comment'
mymanage_site.register(BlogModel, BlogModelAdminSite)

class ChatModelAdminSite(admin.ModelAdmin):
    list_display = ('id', 'title', 'publish', 'read', 'total_like', 'comment_count', 'user_count', 'period', 'created', 'updated')
    list_editable = ('title',)
    search_fields = ('title', 'created')
    ordering = ('-created',)
    actions = ('published', 'unpublished')
    filter_horizontal = ('tags',)
    readonly_fields = ('read', 'total_like', 'comment_count', 'user_count', 'created', 'updated')
    inlines = [CommentInline]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'publish', 'tags', 'period')}),
        ('確認項目', {'fields': ('read', 'total_like', 'comment_count', 'user_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        qs = super(ChatModelAdminSite, self).get_queryset(request).prefetch_related('tags', 'like')
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(ChatModelAdminSite, self).save_model(request, obj, form, change)

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
        return obj.comments.filter(parent__isnull=True).count()
    comment_count.short_description = 'thread'

    def user_count(self, obj):
        return obj.comments.order_by('author').distinct().values_list('author').count()
    user_count.short_description = 'joined'
mymanage_site.register(ChatModel, ChatModelAdminSite)

class CollaboModelAdminSite(admin.ModelAdmin):
    list_display = ('id', 'title', 'publish', 'read', 'total_like', 'comment_count', 'period', 'created', 'updated')
    list_editable = ('title',)
    search_fields = ('title', 'created')
    ordering = ('-created',)
    actions = ('published', 'unpublished')
    filter_horizontal = ('tags',)
    readonly_fields = ('read', 'total_like', 'comment_count', 'created', 'updated')
    inlines = [CommentInline]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'publish', 'tags', 'period')}),
        ('確認項目', {'fields': ('read', 'total_like', 'comment_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        qs = super(CollaboModelAdminSite, self).get_queryset(request).prefetch_related('tags', 'like')
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(CollaboModelAdminSite, self).save_model(request, obj, form, change)

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
        return obj.comments.all().count()
    comment_count.short_description = 'comment'
mymanage_site.register(CollaboModel, CollaboModelAdminSite)

class TodoModelAdminSite(admin.ModelAdmin):
    list_display = ('id', 'title', 'comment_count', 'priority', 'duedate')
    list_editable = ('title', 'priority', 'duedate')
    list_filter = ('priority', 'duedate')
    search_fields = ('title', 'duedate')
    ordering = ('priority', '-duedate')
    actions = ('delete_action',)
    readonly_fields = ('comment_count', 'created', 'updated')
    inlines = [CommentInline]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'priority', 'duedate')}),
        ('確認項目', {'fields': ('comment_count', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        qs = super(TodoModelAdminSite, self).get_queryset(request)
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(TodoModelAdminSite, self).save_model(request, obj, form, change)

    def delete_action(self, request, queryset):
        queryset.delete()
    delete_action.short_description = '削除する'

    def comment_count(self, obj):
        return obj.comments.all().count()
    comment_count.short_description = 'comment'
mymanage_site.register(TodoModel, TodoModelAdminSite)

class FollowModelAdminSite(admin.ModelAdmin):
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
        qs = super(FollowModelAdminSite, self).get_queryset(request)
        return qs.filter(follower=request.user)

    def save_model(self, request, obj, form, change):
        obj.follower = request.user
        super(FollowModelAdminSite, self).save_model(request, obj, form, change)

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
mymanage_site.register(FollowModel, FollowModelAdminSite)

class NotificationAdminSite(admin.ModelAdmin):
    list_display = ('id', 'type_no', 'content_type', 'title', 'confirmed_count', 'delete_count', 'created')
    search_fields = ('type_no', 'created')
    ordering = ('type_no', '-created')
    filter_horizontal = ('confirmed', 'delete')
    readonly_fields = ('content_type', 'title', 'confirmed_count', 'delete_count', 'created')

    # 詳細画面
    fieldsets = [
        ('確認項目', {'fields': ('content_type', 'title', 'confirmed_count', 'delete_count', 'created')}),
    ]

    def get_queryset(self, request):
        qs = super(NotificationAdminSite, self).get_queryset(request)
        return qs.filter(user_from=request.user)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def confirmed_count(self, obj):
        return obj.confirmed.count()
    confirmed_count.short_description = 'confirmed'

    def delete_count(self, obj):
        return obj.delete.count()
    delete_count.short_description = 'delete'

    def title(self, obj):
        return obj.content_object.title
    title.short_description = 'title'
mymanage_site.register(NotificationModel, NotificationAdminSite)

class AdvertiseModelAdminSite(admin.ModelAdmin):
    list_display = ('id', 'title', 'url', 'publish', 'read', 'period', 'created', 'updated')
    list_select_related = ('author',)
    search_fields = ('title', 'created')
    ordering = ('author', 'created')
    actions = ('published', 'unpublished')
    readonly_fields = ('read', 'created', 'updated')

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'url', 'content', 'images', 'videos', 'publish', 'period')}),
        ('確認項目', {'fields': ('read', 'created', 'updated')})
    ]

    def get_queryset(self, request):
        qs = super(AdvertiseModelAdminSite, self).get_queryset(request)
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.type = 1
        super(AdvertiseModelAdminSite, self).save_model(request, obj, form, change)

    def has_add_permission(self, request):
        author = request.user
        if author.is_premium:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        author = request.user
        if author.is_premium:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        author = request.user
        if author.is_premium:
            return True
        return False

    def published(self, request, queryset):
        queryset.update(publish=True)
    published.short_description = '公開する'

    def unpublished(self, request, queryset):
        queryset.update(publish=False)
    unpublished.short_description = '非公開にする'
mymanage_site.register(AdvertiseModel, AdvertiseModelAdminSite)
