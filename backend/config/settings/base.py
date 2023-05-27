"""
Django settings for config project.
Generated by 'django-admin startproject' using Django 4.1.3

For more information on this file, see
https://docs.djangoproject.com/ja/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/ja/4.1/ref/settings/
"""

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/ja/4.1/howto/deployment/checklist/

import os
import environ
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = environ.Path(__file__) - 3

env = environ.Env(DEBUG=(bool, False))
env.read_env(os.path.join(BASE_DIR, '../envs/django.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# Stripe API keys
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')
STRIPE_PUBLIC_KEY = env('STRIPE_PUBLIC_KEY')

# Database
# https://docs.djangoproject.com/ja/4.1/ref/settings/#databases

# pkのデフォルト設定
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# MySQL
DATABASES = {
    'default': {
        'ENGINE': env('MYSQL_ENGINE'),
        'NAME': env('MYSQL_DATABASE'),
        'HOST': env('MYSQL_HOST'),
        'PORT': env('MYSQL_PORT'),
        'USER': env('MYSQL_USER'),
        'PASSWORD': env('MYSQL_PASSWORD'),
    }
}

# Top
INSTALLED_APPS = [
    'daphne'
]

# Application definition
INSTALLED_APPS += [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

# Add Application
INSTALLED_APPS += [
    'apps.myus.apps.ApiConfig',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'channels',
    'django_quill',
    'django_cleanup',
    'import_export',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('JWT',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',)
}

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'templates')],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Channels
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(env('REDIS_HOST'), env('REDIS_PORT'))],
        },
    },
}

ASGI_APPLICATION = 'config.asgi.application'
WSGI_APPLICATION = 'config.wsgi.application'
ROOT_URLCONF = 'config.urls'

AUTH_USER_MODEL = 'myus.User'
AUTHENTICATION_BACKENDS = ['apps.myus.backends.MyBackend']
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'

# humanize カンマ区切り値
NUMBER_GROUPING = 3

# Internationalization
# https://docs.djangoproject.com/ja/4.1/topics/i18n/
TIME_ZONE = 'Asia/Tokyo'
LANGUAGE_CODE = 'ja'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/ja/4.1/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL = 'myus:login'
LOGIN_REDIRECT_URL = 'myus:index'
LOGOUT_REDIRECT_URL = 'myus:login'

# Email
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

# QUILL
QUILL_CONFIGS = {
    'default': {
        'theme': 'snow',
        'modules': {
            'syntax': True,
            'toolbar': [
                [{'header': [1, 2, 3, 4, 5, 6, False]}],
                [{'color': []}, {'background': []}, {'align': []}],
                [{'indent': '+1'}, {'indent': '-1'}, {'list': 'ordered'}, {'list': 'bullet'}],
                ['bold', 'underline', 'strike', 'formula', {'script': 'super'}, {'script': 'sub'}],
                ['code-block', 'blockquote', 'link', 'image'],
            ]
        }
    }
}
