"""
Django settings for themenswall project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'izh37g8zr%j4iyc7=^^wj7uidfr=qz^=4v4v(yy0kvf1+75apy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'users.apps.UsersConfig',
    'feed.apps.FeedConfig',
    'crispy_forms',
    'stdimage',
    'products',
    'orders',
    'sslserver',
    'channels',
]
ASGI_APPLICATION = "themenswall.routing.application"
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]
# 'whitenoise.middleware.WhiteNoiseMiddleware',
    
ROOT_URLCONF = 'themenswall.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'feed.views.CountNotifications',
                'feed.views.GetProfile',
                'products.context_processors.menu_links',

            ],
        },
    },
]
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.pubsub.RedisPubSubChannelLayer",
#         "CONFIG": {
#             "hosts": [("localhost", 6379)],
#         },
#     },
# }

WSGI_APPLICATION = 'themenswall.wsgi.application'
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
# if DEBUG:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# else:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'themenswall',
        'USER': 'admin',
        'PASSWORD': 'Admin@123',
        'HOST': 'localhost',
        'PORT': '',
    }
    }

DEFAULT_AUTO_FIELD='django.db.models.AutoField'


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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
STATIC_URL = '/static/'
# STATICFILES_DIRS =[os.path.join(BASE_DIR, 'static')]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'live-static', 'media-root')



CRISPY_TEMPLATE_PACK = 'bootstrap4'

# LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'mikcraft1995@gmail.com'
# EMAIL_HOST_PASSWORD = 'irdcudexygqgvjzw'
AUTH_USER_MODEL = 'users.CustomeUser'
HOST_URL = "http://127.0.0.1:8000/"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'development0261@gmail.com'
EMAIL_HOST_PASSWORD = 'asrifdxrcoogeola'

if DEBUG:
    MY_DOMAIN = 'http://127.0.0.1:8000'
else:
    MY_DOMAIN = "https://themes-wall.herokuapp.com/"
STRIPE_PUBLIC_KEY='pk_test_51JKwEbKoFJGBw6J3m1AMEmqZ2jVymec4dq7dSXfP7T3UZUzVL8mIHpdo4fzmen9Ty5yp5BofMwai50eWHSq3veel00PR6OxzBA'
STRIPE_PRIVATE_KEY='sk_test_51JKwEbKoFJGBw6J3mspY8S8d3xHUjwsrXayaWRnS3oflu2VInkpokZwenrAyoGZno4jRmgzJglPCq73Yzgt9UDrR00g0Xivm3R'
STRIPE_ENDPOINT_SECRET = ''
