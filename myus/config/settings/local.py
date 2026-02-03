from config.settings.base import *


DEBUG = True
ALLOWED_HOSTS = ["*"]
INTERNAL_IPS = ["127.0.0.1", "https://my-us.vercel.app/"]

# Add Application
INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

# Cors headers
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True
