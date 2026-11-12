from config.env import env
from config.settings.base import *

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
SECURE_HSTS_SECONDS = 3600

# Email
MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.smtp.EmailBackend",
        "OPTIONS": {
            "host": env.email_host,
            "port": env.email_port,
            "username": env.email_host_user,
            "password": env.email_host_password,
            "use_tls": True,
            "timeout": 10,
        },
    },
}

# Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://:{env.redis_password}@{env.redis_host}:{env.redis_port}/1",
    },
}
