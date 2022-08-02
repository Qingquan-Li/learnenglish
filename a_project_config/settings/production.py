"""
Applying migrations to database:
$ python manage.py migrate --settings=a_project_config.settings.production

Creating an admin user:
$ python manage.py createsuperuser --settings=a_project_config.settings.production

Running tests:
$ python manage.py test --settings=a_project_config.settings.production
"""


import os
from pathlib import Path

from dotenv import load_dotenv

# https://saurabh-kumar.com/python-dotenv/
load_dotenv()  # take environment variables from .env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
# a_project_config.settings --> a_project_config.settings.base
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'xxx'  # Original auto-generated SECRET_KEY
# https://docs.djangoproject.com/en/3.2/ref/settings/#secret-key
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = False

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['learnenglish.qingquanli.com', 'localhost', ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',  # new

    # 3rd party
    'rest_framework',
    'corsheaders',
    'ckeditor',
    'django.contrib.postgres',

    # Local
    'accounts.apps.AccountsConfig',
    'words_in_sentences.apps.WordsInSentencesConfig',
    'homepage.apps.HomepageConfig',
    'writing.apps.WritingConfig',
    'speech.apps.SpeechConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # new
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'a_project_config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [],
        # docs.djangoproject.com/zh-hans/3.2/intro/tutorial03/#write-views-that-actually-do-something
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],  # new
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

WSGI_APPLICATION = 'a_project_config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'learnenglish',
        'USER': 'learnenglish',
        'PASSWORD': os.getenv('PRODUCTION_POSTGRESQL_PASSWORD'),
        # https://docs.djangoproject.com/en/3.2/ref/settings/#host
        # default (empty HOST), the connection to the database is done through UNIX domain sockets.
        # If you want to connect through TCP sockets, set HOST to ‘localhost’ or ‘127.0.0.1’.
        'HOST': 'localhost',
        'PORT': '5432',
    },
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# #################### Newly expanded content ####################


# docs.djangoproject.com/en/3.2/topics/auth/customizing/#substituting-a-custom-user-model
AUTH_USER_MODEL = 'accounts.CustomUser'


# https://docs.djangoproject.com/en/3.2/howto/static-files/
# During development, if you use django.contrib.staticfiles,
# this will be done automatically by runserver when DEBUG is set to True
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# DRF default settings is in:
# .venv/lib/python3.8/site-packages/rest_framework/settings.py
# Setting the global throttling policy:
# https://www.django-rest-framework.org/api-guide/throttling/
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        # anonymous users. The IP address of the request will be used as the unique cache key.
        'anon': '60/minute',
        # given user. The user id will be used as a unique cache key if the user is authenticated.
        'user': '600/minute',
    },
}

# # https://github.com/adamchainz/django-cors-headers
# CORS_ALLOWED_ORIGINS = [
#     # 3000 is the default port for React
#     'http://localhost:3000',
#     # 8080 is the default port for Vue
#     # 'http://localhost:8080',
# ]
