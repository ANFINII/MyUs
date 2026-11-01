from config.settings.base import *
from config.env import env

DEBUG = False

# CSRF
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "Lax"

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "Lax"

# Security
# https://docs.djangoproject.com/ja/5.0/ref/settings/
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
NINJA_NUM_PROXIES = 1
SECURE_SSL_REDIRECT = True

# Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://:{env.redis_password}@{env.redis_host}:{env.redis_port}/1",
    },
}
