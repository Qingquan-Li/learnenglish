"""
Runserver:
$ python manage.py runserver 0:8000 --settings=a_project_config.settings.local

Creating an admin user:
$ python manage.py createsuperuser --settings=a_project_config.settings.local

Creating new migrations based on models:
$ python manage.py makemigrations [app_name] --settings=a_project_config.settings.local

Applying migrations to database:
$ python manage.py migrate --settings=a_project_config.settings.local

Running the collectstatic management command:
$ python manage.py collectstatic --settings=a_project_config.settings.local

Running tests:
$ python manage.py test --settings=a_project_config.settings.local
"""


import os

from .production import *  # noqa

# DEBUG = False  # Unable to load static files automatically
DEBUG = True

ALLOWED_HOSTS = ['*']


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'learnenglish',
        'USER': 'learnenglish',  # Or: postgres
        'PASSWORD': os.getenv('LOCAL_POSTGRESQL_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
