from .base import *

DEBUG = False
ALLOWED_HOSTS = ['myus.com']

# Security
# https://docs.djangoproject.com/ja/4.0/ref/settings/
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
