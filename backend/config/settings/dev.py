from config.settings.base import *

DEBUG = True
ALLOWED_HOSTS = ['dev.myus.com']
INTERNAL_IPS = ['192.168.33.1', '192.168.1.65']

# Add Application
INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# CSRF
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'Lax'

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Security
# https://docs.djangoproject.com/ja/5.0/ref/settings/
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
