from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import User, MyPage, SearchTag, Tag, FollowModel, Comment
from .models import VideoModel, LiveModel, MusicModel, PictureModel, BlogModel, ChatModel, CollaboModel, TodoModel

# Admin用の管理画面
class MyPageInline(admin.TabularInline):
    model = MyPage
    extra = 0
    readonly_fields = ('author', 'read', 'updated')
    verbose_name_plural = 'Myページ情報'
    
class SearchTagInline(admin.TabularInline):
    model = SearchTag
    extra = 1
    max_num = 10
    verbose_name_plural = '検索タグ'
    
class CommentInlineAdmin(GenericTabularInline):
    model = Comment
    extra = 0
    max_num = 100
    readonly_fields = ('total_like',)
    verbose_name_plural = 'コメント'

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'いいね数'
    
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'nickname', 'full_name', 'birthday', 'age', 'gender', 'phone')
    list_filter = ('birthday', 'gender')
    search_fields = ('username', 'email', 'nickname', 'full_name', 'phone')
    ordering = ('id',)
    filter_horizontal = ('groups', 'user_permissions')
    inlines = [MyPageInline, SearchTagInline]
    
    # 詳細画面
    readonly_fields = ('full_name', 'birthday', 'age', 'date_joined', 'last_login')
    fieldsets = [
        ('アカウント情報', {'fields': ('user_image', 'username', 'email', 'nickname', 'full_name', 'birthday', 'age', 'gender', 'phone', 'location', 'profession', 'introduction', 'groups', 'user_permissions')}),
        ('権限情報', {'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser', 'date_joined', 'last_login')})
    ]
    
@admin.register(FollowModel)
class FollowModelAdmin(admin.ModelAdmin):
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

@admin.register(SearchTag)
class SearchTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'sequence', 'searchtag')
    list_select_related = ('author',)
    search_fields = ('author__nickname', 'searchtag')
    ordering = ('author', 'sequence')

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('sequence', 'searchtag')}),
    ]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(TagAdmin, self).save_model(request, obj, form, change)
    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'tag',)
    search_fields = ('author__nickname', 'tag',)
    ordering = ('author', 'tag',)

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('tag',)}),
    ]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(TagAdmin, self).save_model(request, obj, form, change)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_type', 'object_id', 'content_object', 'author', 'text', 'parent_id', 'total_like', 'created', 'updated')
    list_select_related = ('author', 'parent')
    search_fields = ('text', 'author__nickname', 'created', 'updated')
    ordering = ('content_type', 'object_id', 'id')
    filter_horizontal = ('like',)
    readonly_fields = ('total_like', 'created', 'updated')

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('author', 'parent', 'text', 'like', 'content_type', 'object_id')}),
        ('確認項目', {'fields': ('total_like', 'created', 'updated')})
    ]

@admin.register(VideoModel)
class VideoModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'publish', 'read', 'total_like', 'created', 'updated')
    list_select_related = ('author',)
    search_fields = ('title', 'author__nickname', 'created')
    ordering = ('author', '-created')
    filter_horizontal = ('tags', 'like')
    readonly_fields = ('total_like', 'created', 'updated')
    inlines = [CommentInlineAdmin]
    
    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'images', 'videos', 'publish', 'tags', 'like', 'read')}),
        ('確認項目', {'fields': ('total_like', 'created', 'updated')})
    ]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(VideoModelAdmin, self).save_model(request, obj, form, change)

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'

@admin.register(LiveModel)
class LiveModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'publish', 'read', 'total_like', 'created', 'updated')
    list_select_related = ('author',)
    search_fields = ('title', 'author__nickname', 'created')
    ordering = ('author', '-created')
    filter_horizontal = ('tags', 'like')
    readonly_fields = ('total_like', 'created', 'updated')
    inlines = [CommentInlineAdmin]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'images', 'lives', 'publish', 'tags', 'like', 'read')}),
        ('確認項目', {'fields': ('total_like', 'created', 'updated')})
    ]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(LiveModelAdmin, self).save_model(request, obj, form, change)
    
    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'
    
@admin.register(MusicModel)
class MusicModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'publish', 'read', 'total_like', 'created', 'updated')
    list_select_related = ('author',)
    search_fields = ('title', 'author__nickname', 'created')
    ordering = ('author', '-created')
    filter_horizontal = ('tags', 'like')
    readonly_fields = ('total_like', 'created', 'updated')
    inlines = [CommentInlineAdmin]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'lyrics', 'musics', 'publish', 'tags', 'like', 'read')}),
        ('確認項目', {'fields': ('total_like', 'created', 'updated')})
    ]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(MusicModelAdmin, self).save_model(request, obj, form, change)
    
    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'
    
@admin.register(PictureModel)
class PictureModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'publish', 'read', 'total_like', 'created', 'updated')
    list_select_related = ('author',)
    search_fields = ('title', 'author__nickname', 'created')
    ordering = ('author', '-created')
    filter_horizontal = ('tags', 'like')
    readonly_fields = ('total_like', 'created', 'updated')
    inlines = [CommentInlineAdmin]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'images', 'publish', 'tags', 'like', 'read')}),
        ('確認項目', {'fields': ('total_like', 'created', 'updated')})
    ]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(PictureModelAdmin, self).save_model(request, obj, form, change)

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'
    
@admin.register(BlogModel)
class BlogModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'publish', 'read', 'total_like', 'created', 'updated')
    list_select_related = ('author',)
    search_fields = ('title', 'author__nickname', 'created')
    ordering = ('author', '-created')
    filter_horizontal = ('tags', 'like')
    readonly_fields = ('total_like', 'created', 'updated')
    inlines = [CommentInlineAdmin]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'images', 'richtext', 'publish', 'tags', 'like', 'read')}),
        ('確認項目', {'fields': ('total_like', 'created', 'updated')})
    ]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(BlogModelAdmin, self).save_model(request, obj, form, change)

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'
    
@admin.register(ChatModel)
class ChatModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'publish', 'read', 'total_like', 'created', 'updated')
    list_select_related = ('author',)
    search_fields = ('title', 'author__nickname', 'created')
    ordering = ('author', '-created')
    filter_horizontal = ('tags', 'like')
    readonly_fields = ('total_like', 'created', 'updated')
    inlines = [CommentInlineAdmin]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'publish', 'tags', 'like', 'read')}),
        ('確認項目', {'fields': ('total_like', 'created', 'updated')})
    ]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(ChatModelAdmin, self).save_model(request, obj, form, change)
    
    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'
    
@admin.register(CollaboModel)
class CollaboModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'publish', 'read', 'total_like', 'created', 'updated')
    list_select_related = ('author',)
    search_fields = ('title', 'author__nickname', 'created')
    ordering = ('author', '-created')
    filter_horizontal = ('tags', 'like')
    readonly_fields = ('total_like', 'created', 'updated')
    inlines = [CommentInlineAdmin]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'publish', 'tags', 'like', 'read')}),
        ('確認項目', {'fields': ('total_like', 'created', 'updated')})
    ]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(CollaboModelAdmin, self).save_model(request, obj, form, change)
    
    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'

@admin.register(TodoModel)
class TodoModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'priority', 'duedate')
    list_select_related = ('author',)
    list_filter = ('priority', 'duedate')
    search_fields = ('title', 'author__nickname', 'priority', 'duedate')
    ordering = ('author', 'priority', '-duedate')
    readonly_fields = ('created', 'updated')
    inlines = [CommentInlineAdmin]
    
    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'priority', 'duedate')}),
        ('確認項目', {'fields': ('created', 'updated')})
    ]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(TodoModelAdmin, self).save_model(request, obj, form, change)

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

mypage_site = MyUsAdminSite(name='mypage')
mypage_site.disable_action('delete_selected')

class FollowModelAdminSite(admin.ModelAdmin):
    list_display = ('id', 'following', 'created')
    list_select_related = ('following',)
    search_fields = ('following__nickname', 'following__introduction', 'created')
    ordering = ('following', '-created')
    readonly_fields = ('following', 'created')

    # 詳細画面
    fieldsets = [
        ('確認項目', {'fields': ('following', 'following_introduction', 'created')})
    ]
    
    def save_model(self, request, obj, form, change):
        obj.follower = request.user
        super(FollowModelAdminSite, self).save_model(request, obj, form, change)
        
    def get_queryset(self, request): 
        qs = super(FollowModelAdminSite, self).get_queryset(request) 
        return qs.filter(follower=request.user)
    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def following_introduction(self, obj):
        return obj.following.introduction
    following_introduction.short_description = 'Introduction'
mypage_site.register(FollowModel, FollowModelAdminSite)

class SearchTagAdminSite(admin.ModelAdmin):
    list_display = ('id', 'sequence', 'searchtag')
    list_editable = ('sequence', 'searchtag',)
    list_per_page = 10
    search_fields = ('searchtag',)
    ordering = ('sequence',)
    
    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('sequence', 'searchtag')}),
    ]
    
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(SearchTagAdminSite, self).save_model(request, obj, form, change)

    def get_queryset(self, request): 
        qs = super(SearchTagAdminSite, self).get_queryset(request) 
        return qs.filter(author=request.user)
mypage_site.register(SearchTag, SearchTagAdminSite)

class TagAdminSite(admin.ModelAdmin):
    list_display = ('id', 'tag',)
    search_fields = ('tag',)
    ordering = ('tag',)

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('tag',)}),
    ]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(TagAdminSite, self).save_model(request, obj, form, change)

    def get_queryset(self, request): 
        qs = super(TagAdminSite, self).get_queryset(request) 
        return qs.filter(author=request.user)
mypage_site.register(Tag, TagAdminSite)

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

class VideoModelAdminSite(admin.ModelAdmin):
    list_display = ('id', 'title', 'publish', 'read', 'total_like', 'created', 'updated')
    list_editable = ('title',)
    search_fields = ('title', 'created')
    ordering = ('-created',)
    actions = ('published', 'unpublished')
    filter_horizontal = ('tags',)
    readonly_fields = ('read', 'total_like', 'created', 'updated')
    inlines = [CommentInline]
    
    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'images', 'videos', 'publish', 'tags')}),
        ('確認項目', {'fields': ('read', 'total_like', 'created', 'updated')})
    ]
    
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(VideoModelAdminSite, self).save_model(request, obj, form, change)

    def published(self, request, queryset):
        queryset.update(publish=True)
    published.short_description = '公開する'
    
    def unpublished(self, request, queryset):
        queryset.update(publish=False)
    unpublished.short_description = '非公開にする'

    def get_queryset(self, request): 
        qs = super(VideoModelAdminSite, self).get_queryset(request) 
        return qs.filter(author=request.user)
    
    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'
mypage_site.register(VideoModel, VideoModelAdminSite)

class LiveModelAdminSite(admin.ModelAdmin):
    list_display = ('id', 'title', 'publish', 'read', 'total_like', 'created', 'updated')
    list_editable = ('title',)
    search_fields = ('title', 'created')
    ordering = ('-created',)
    actions = ('published', 'unpublished')
    filter_horizontal = ('tags',)
    readonly_fields = ('read', 'total_like', 'created', 'updated')
    inlines = [CommentInline]
    
    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'images', 'lives', 'publish', 'tags')}),
        ('確認項目', {'fields': ('read', 'total_like', 'created', 'updated')})
    ]
    
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(LiveModelAdminSite, self).save_model(request, obj, form, change)

    def published(self, request, queryset):
        queryset.update(publish=True)
    published.short_description = '公開する'
    
    def unpublished(self, request, queryset):
        queryset.update(publish=False)
    unpublished.short_description = '非公開にする'

    def get_queryset(self, request): 
        qs = super(LiveModelAdminSite, self).get_queryset(request) 
        return qs.filter(author=request.user)

    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'
mypage_site.register(LiveModel, LiveModelAdminSite)

class MusicModelAdminSite(admin.ModelAdmin):
    list_display = ('id', 'title', 'publish', 'read', 'total_like', 'created', 'updated')
    list_editable = ('title',)
    search_fields = ('title', 'created')
    ordering = ('-created',)
    actions = ('published', 'unpublished')
    filter_horizontal = ('tags',)
    readonly_fields = ('read', 'total_like', 'created', 'updated')
    inlines = [CommentInline]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'lyrics', 'musics', 'publish', 'tags')}),
        ('確認項目', {'fields': ('read', 'total_like', 'created', 'updated')})
    ]
    
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(MusicModelAdminSite, self).save_model(request, obj, form, change)

    def published(self, request, queryset):
        queryset.update(publish=True)
    published.short_description = '公開する'
    
    def unpublished(self, request, queryset):
        queryset.update(publish=False)
    unpublished.short_description = '非公開にする'

    def get_queryset(self, request): 
        qs = super(MusicModelAdminSite, self).get_queryset(request) 
        return qs.filter(author=request.user)
    
    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'
mypage_site.register(MusicModel, MusicModelAdminSite)

class PictureModelAdminSite(admin.ModelAdmin):
    list_display = ('id', 'title', 'publish', 'read', 'total_like', 'created', 'updated')
    list_editable = ('title',)
    search_fields = ('title', 'created')
    ordering = ('-created',)
    actions = ('published', 'unpublished')
    filter_horizontal = ('tags',)
    readonly_fields = ('read', 'total_like', 'created', 'updated')
    inlines = [CommentInline]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'images', 'publish', 'tags')}),
        ('確認項目', {'fields': ('read', 'total_like', 'created', 'updated')})
    ]
    
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(PictureModelAdminSite, self).save_model(request, obj, form, change)

    def published(self, request, queryset):
        queryset.update(publish=True)
    published.short_description = '公開する'
    
    def unpublished(self, request, queryset):
        queryset.update(publish=False)
    unpublished.short_description = '非公開にする'

    def get_queryset(self, request): 
        qs = super(PictureModelAdminSite, self).get_queryset(request) 
        return qs.filter(author=request.user)
    
    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'
mypage_site.register(PictureModel, PictureModelAdminSite)

class BlogModelAdminSite(admin.ModelAdmin):
    list_display = ('id', 'title', 'publish', 'read', 'total_like', 'created', 'updated')
    list_editable = ('title',)
    search_fields = ('title', 'created')
    ordering = ('-created',)
    actions = ('published', 'unpublished')
    filter_horizontal = ('tags',)
    readonly_fields = ('read', 'total_like', 'created', 'updated')
    inlines = [CommentInline]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'images', 'richtext', 'publish', 'tags')}),
        ('確認項目', {'fields': ('read', 'total_like', 'created', 'updated')})
    ]
    
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(BlogModelAdminSite, self).save_model(request, obj, form, change)

    def published(self, request, queryset):
        queryset.update(publish=True)
    published.short_description = '公開する'
    
    def unpublished(self, request, queryset):
        queryset.update(publish=False)
    unpublished.short_description = '非公開にする'

    def get_queryset(self, request): 
        qs = super(BlogModelAdminSite, self).get_queryset(request) 
        return qs.filter(author=request.user)
    
    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'
mypage_site.register(BlogModel, BlogModelAdminSite)

class ChatModelAdminSite(admin.ModelAdmin):
    list_display = ('id', 'title', 'publish', 'read', 'total_like', 'created', 'updated')
    list_editable = ('title',)
    search_fields = ('title', 'created')
    ordering = ('-created',)
    actions = ('published', 'unpublished')
    filter_horizontal = ('tags',)
    readonly_fields = ('read', 'total_like', 'created', 'updated')
    inlines = [CommentInline]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'publish', 'tags')}),
        ('確認項目', {'fields': ('read', 'total_like', 'created', 'updated')})
    ]
    
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(ChatModelAdminSite, self).save_model(request, obj, form, change)

    def published(self, request, queryset):
        queryset.update(publish=True)
    published.short_description = '公開する'
    
    def unpublished(self, request, queryset):
        queryset.update(publish=False)
    unpublished.short_description = '非公開にする'

    def get_queryset(self, request): 
        qs = super(ChatModelAdminSite, self).get_queryset(request) 
        return qs.filter(author=request.user)
    
    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'
mypage_site.register(ChatModel, ChatModelAdminSite)

class CollaboModelAdminSite(admin.ModelAdmin):
    list_display = ('id', 'title', 'publish', 'read', 'total_like', 'created', 'updated')
    list_editable = ('title',)
    search_fields = ('title', 'created')
    ordering = ('-created',)
    actions = ('published', 'unpublished')
    filter_horizontal = ('tags',)
    readonly_fields = ('read', 'total_like', 'created', 'updated')
    inlines = [CommentInline]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'publish', 'tags')}),
        ('確認項目', {'fields': ('read', 'total_like', 'created', 'updated')})
    ]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(CollaboModelAdminSite, self).save_model(request, obj, form, change)

    def published(self, request, queryset):
        queryset.update(publish=True)
    published.short_description = '公開する'

    def unpublished(self, request, queryset):
        queryset.update(publish=False)
    unpublished.short_description = '非公開にする'

    def get_queryset(self, request): 
        qs = super(CollaboModelAdminSite, self).get_queryset(request) 
        return qs.filter(author=request.user)
    
    def total_like(self, obj):
        return obj.like.count()
    total_like.short_description = 'like'
mypage_site.register(CollaboModel, CollaboModelAdminSite)

class TodoModelAdminSite(admin.ModelAdmin):
    list_display = ('id', 'title', 'priority', 'duedate', 'created', 'updated')
    list_editable = ('title', 'priority', 'duedate')
    list_filter = ('priority', 'duedate')
    search_fields = ('title', 'duedate')
    ordering = ('priority', 'duedate')
    readonly_fields = ('created', 'updated')
    inlines = [CommentInline]

    # 詳細画面
    fieldsets = [
        ('編集項目', {'fields': ('title', 'content', 'priority', 'duedate')}),
        ('確認項目', {'fields': ('created', 'updated')})
    ]
    
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(TodoModelAdminSite, self).save_model(request, obj, form, change)
    
    def get_queryset(self, request): 
        qs = super(TodoModelAdminSite, self).get_queryset(request) 
        return qs.filter(author=request.user)
mypage_site.register(TodoModel, TodoModelAdminSite)