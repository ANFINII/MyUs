class DeferData:
    user = [
        'password',
        'email',
        'username',
        'is_superuser',
        'is_active',
        'last_login',
        'date_joined',
    ]

    author = [
        'author__password',
        'author__email',
        'author__username',
        'author__is_superuser',
        'author__is_active',
        'author__is_staff',
        'author__last_login',
        'author__date_joined',
    ]

    profile = [
        'password',
        'is_superuser',
        'is_active',
        'is_staff',
        'last_login',
        'date_joined',
        'profile__user_id',
    ]

    mypage = [
        'password',
        'email',
        'username',
        'is_superuser',
        'is_active',
        'is_staff',
        'last_login',
        'date_joined',
        'mypage__user_id',
    ]

    follow = [
        'follower__password',
        'follower__email',
        'follower__username',
        'follower__is_superuser',
        'follower__is_active',
        'follower__is_staff',
        'follower__last_login',
        'follower__date_joined',
    ]

    models = [
        'content',
        'updated',
    ]

    defer_list = models + author
