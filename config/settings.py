"""
Django settings for config project.
Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/ja/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/ja/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/ja/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '53*2!!yd=rna4=0n(mgtiesedwjv2q&vlcm051czesxyn=%!ab'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Add Application
INSTALLED_APPS += [
    'myusapp.apps.MyusappConfig',
    'django.contrib.humanize',
    'django_cleanup',
    'debug_toolbar',
    'import_export',
    'markdownx',
    'ckeditor',
    'ckeditor_uploader',
    'channels',
]

NUMBER_GROUPING = 3

AUTH_USER_MODEL = 'myusapp.User'

AUTHENTICATION_BACKENDS = [
    'myusapp.backends.MyBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
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
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/ja/3.0/ref/settings/#databases

# sqlite3用の設定
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/ja/3.0/topics/i18n/
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/ja/3.0/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CKEDITOR
CKEDITOR_UPLOAD_PATH = 'images/upload_images'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_RESTRICT_BY_DATE = False
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_UPLOAD_SLUGIFY_FILENAME = False

# CKEDITOR_CONFIGS = {
#     'default': {
#         'toolbar': 'Custom',
#         'width': '100%',
#         'height': '300px',
#         'contentsCss': 'img { max-width: 100%; height: auto !important;}',
#         'toolbar_Custom': [
#             ['Styles', 'Format'],
#             ['Bold', 'Link', 'Image'],
#         ],
#     },
# }

CKEDITOR_CONFIGS = {
    'default': {
        # 'skin': 'moono',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',

            ]},
        ],
    }
}
    #     'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
    #     # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
    #     # 'height': 291,
    #     # 'width': '100%',
    #     # 'filebrowserWindowHeight': 725,
    #     # 'filebrowserWindowWidth': 940,
    #     # 'toolbarCanCollapse': True,
    #     # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
    #     'tabSpaces': 4,
    #     'extraPlugins': ','.join([
    #         'uploadimage', # the upload image feature
    #         # your extra plugins here
    #         'div',
    #         'autolink',
    #         'autoembed',
    #         'embedsemantic',
    #         'autogrow',
    #         # 'devtools',
    #         'widget',
    #         'lineutils',
    #         'clipboard',
    #         'dialog',
    #         'dialogui',
    #         'elementspath'
    #     ]),
    # }
# }

# Channels
ASGI_APPLICATION = 'config.asgi.application'
