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
SECURE_PROXY_SSL_HEADER = ("HTTP_CLOUDFRONT_FORWARDED_PROTO", "https")
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

# Media
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "bucket_name": env.aws_storage_bucket_name,
            "region_name": env.aws_s3_region_name,
            "custom_domain": env.media_domain,
            "querystring_auth": False,
            "file_overwrite": False,
        },
    },
    "private": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "bucket_name": env.hires_bucket_name,
            "region_name": env.aws_s3_region_name,
            "querystring_auth": True,
            "querystring_expire": PRIVATE_URL_EXPIRE,
            "file_overwrite": False,
        },
    },
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}
MEDIA_BASE_URL = f"https://{env.media_domain}/"
