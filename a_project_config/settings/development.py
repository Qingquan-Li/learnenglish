"""
Applying migrations to database:
$ python manage.py migrate --settings=a_project_config.settings.development

Creating an admin user:
$ python manage.py createsuperuser --settings=a_project_config.settings.development

Running tests:
$ python manage.py test --settings=a_project_config.settings.development

Runserver:
$ python manage.py runserver 0:8000 --settings=a_project_config.settings.development
"""


import os

from dotenv import load_dotenv

from .production import *  # noqa

# https://saurabh-kumar.com/python-dotenv/
load_dotenv()  # take environment variables from .env

# DEBUG = False  # Unable to load static files automatically
DEBUG = True

ALLOWED_HOSTS = [os.getenv('SERVER_IP'), 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'learnenglish_dev',
        'USER': 'learnenglish_dev',
        'PASSWORD': os.getenv('DEVELOPMENT_POSTGRESQL_PASSWORD'),
        # https://docs.djangoproject.com/en/3.2/ref/settings/#host
        # default (empty HOST), the connection to the database is done through UNIX domain sockets.
        # If you want to connect through TCP sockets, set HOST to ‘localhost’ or ‘127.0.0.1’.
        'HOST': 'localhost',
        'PORT': '5432',
    },
}
