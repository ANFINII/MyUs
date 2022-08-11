"""
Django settings for config project.
Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/ja/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/ja/4.0/ref/settings/
"""

import os
import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = environ.Path(__file__) - 3

env = environ.Env(DEBUG=(bool, False))
env.read_env(os.path.join(BASE_DIR, 'envs/.django'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/ja/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# Stripe API keys
STRIPE_PUBLIC_KEY = env('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')

# Database
# https://docs.djangoproject.com/ja/4.0/ref/settings/#databases

# pkのデフォルト設定
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# MySQL
DATABASES = {
    'default': {
        'ENGINE': env('MYSQL_ENGINE'),
        'NAME': env('MYSQL_DATABASE'),
        'USER': env('MYSQL_USER'),
        'PASSWORD': env('MYSQL_PASSWORD'),
        'HOST': env('MYSQL_HOST'),
        'PORT': env('MYSQL_PORT'),
    }
}

# Application definition
INSTALLED_APPS = [
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
    'corsheaders',
    'channels',
    'ckeditor',
    'ckeditor_uploader',
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
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
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

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# Channels
ASGI_APPLICATION = 'config.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(env('REDIS_HOST'), env('REDIS_PORT'))],
        },
    },
}

AUTH_USER_MODEL = 'myus.User'
AUTHENTICATION_BACKENDS = ['apps.myus.backends.MyBackend']
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# humanize カンマ区切り値
NUMBER_GROUPING = 3

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
# https://docs.djangoproject.com/ja/4.0/topics/i18n/
TIME_ZONE = 'Asia/Tokyo'
LANGUAGE_CODE = 'ja'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/ja/4.0/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL = 'myus:login'
LOGIN_REDIRECT_URL = 'myus:index'
LOGOUT_REDIRECT_URL = 'myus:login'

# CKEDITOR
CKEDITOR_UPLOAD_PATH = 'images/upload_images'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_RESTRICT_BY_DATE = False
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_UPLOAD_SLUGIFY_FILENAME = False
CKEDITOR_CONFIGS = {
   'default': {
       'toolbar_Full': [
            ['Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['Image', 'Table', 'HorizontalRule'],
            ['Source'],
            ['Undo', 'Redo'],
            ['Maximize'],
        ],
        'width': '100%',
        'extraPlugins': 'justify,liststyle,indent',
   },
}
