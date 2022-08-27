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
