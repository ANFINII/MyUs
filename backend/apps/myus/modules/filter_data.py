class DeferData:
    user = [
        'user__password',
        'user__email',
        'user__username',
        'user__is_superuser',
        'user__is_active',
        'user__is_admin',
        'user__last_login',
        'user__date_joined',
    ]

    author = [
        'author__password',
        'author__email',
        'author__username',
        'author__is_superuser',
        'author__is_active',
        'author__is_admin',
        'author__last_login',
        'author__date_joined',
    ]

    follow = [
        'follower__password',
        'follower__email',
        'follower__username',
        'follower__is_superuser',
        'follower__is_active',
        'follower__is_admin',
        'follower__last_login',
        'follower__date_joined',
    ]

    models = [
        'content',
        'updated',
    ]

    defer_list = models + author
