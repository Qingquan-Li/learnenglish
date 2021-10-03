# Runserver:
# $ python manage.py runserver 0:8000 --settings=a_project_config.settings.local

# Applying migrations to database:
# $ python manage.py migrate --settings=a_project_config.settings.local

# Running the collectstatic management command:
# $ python manage.py collectstatic --settings=a_project_config.settings.local

# Creating an admin user:
# python manage.py createsuperuser --settings=a_project_config.settings.local

import os

from .base import *  # noqa

# DEBUG = False  # Unable to load static files automatically
DEBUG = True

ALLOWED_HOSTS = ['*']


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Local MySQL:
# https://docs.djangoproject.com/en/3.2/ref/databases/#mysql-db-api-drivers
# $ pip install mysqlclient
# mysqlclient with mysql-8.0.26-macos11-arm64: NameError: name '_mysql' is not defined
# stackoverflow.com/questions/63109987/nameerror-name-mysql-is-not-defined-after-setting-change-to-mysql
import pymysql  # noqa
pymysql.install_as_MySQLdb()
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'learnenglish',
        'USER': 'root',
        'PASSWORD': os.getenv('LOCAL_MYSQL_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
