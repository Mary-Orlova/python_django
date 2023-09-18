"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as __
import sentry_sdk


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
#
# Подключение пакета Sentry SDK + ссылка индивидуальная, ее нельзя афишировать_через нее приходят уведомления
sentry_sdk.init(
dsn="https://0cc328ab19e60065433c2f3c39bc93ba@o4505727550357504.ingest.sentry.io/4505727579389952",
traces_sample_rate=1.0,
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-hvxn%qq=gyw^4*o2lo1#bw0=wh#ux9s8h!=@c608arf_gz3+^7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Хосты внутренний - нули для подключения локального сервера 127
ALLOWED_HOSTS = [
    '0.0.0.0',
    '127.0.0.1',
]
# конфигурация Internal IPs
INTERNAL_IPS = [
    '127.0.0.1',
]

# важно, что бы данный код работал только в режиме дебаг
if DEBUG:
    import socket
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS.append('10.0.2.2')
    INTERNAL_IPS.extend(
        [ip[: ip.rfind('.')] + '.1' for ip in ips]
    )


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    # подключение django-debug-toolbar
    'debug_toolbar',
    'django.contrib.staticfiles',

    'django.contrib.sitemaps',
    'shopapp.apps.ShopappConfig',
    'myauth.apps.MyauthConfig',
    'requestdataapp.apps.RequestdataappConfig',
    "rest_framework",
    'django_filters',
    'myapiapp.apps.MyapiappConfig',
    'drf_spectacular',
    'blogapp.apps.BlogappConfig',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'requestdataapp.middlewares.set_useragent_onrequest_middleware',
    'requestdataapp.middlewares.CountRequestsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    # для django-debug-toolbar
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        # Первые три строки подключение шаблонов для django-debug-toolbar
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

USE_L1ON = True

LOCALE_PATHS = [
    BASE_DIR / 'locale/'
]

LANGUAGES = [
    ('en', __('English')),
    ('ru', __('Russian')),
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'uploads'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = reverse_lazy("myauth:about-me")
LOGIN_URL = reverse_lazy("myauth:login")
# Размер логов для хранения в файле в базовой директории с названием log.txt (3 штуки)
LOGFILE_NAME = BASE_DIR / 'log.txt'
LOGFILE_SIZE = 1 * 1024 * 1024
LOGFILE_COUNT = 3

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] %(name)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'logfile': {
            'class': 'logging.handlers.RotatingFileHandler',
            # 'class': 'logging.handlers.TimeRotatingFileHandler',
            # ротация по дням выше код
            'filename': LOGFILE_NAME,
            'maxBytes': LOGFILE_SIZE,
            'backupCount': LOGFILE_COUNT,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': [
            'console',
            'logfile',
        ],
        'level': 'INFO',
        # 'level': 'DEBUG',

    },
}


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_SCHEME_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'My Site Project API',
    'DESCRIPTION': 'My site with shop app and custom auth',
    'VERSION': '1.0.0.',
    'SERVE_INCLUDE_SCHEMA': False,
}