from config.settings.base import *

DEBUG = False

# Security
# https://docs.djangoproject.com/ja/4.1/ref/settings/
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
