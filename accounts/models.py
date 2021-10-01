# docs.djangoproject.com/en/3.2/topics/auth/customizing/#substituting-a-custom-user-model
# Creating the custom User model and point AUTH_USER_MODEL to it in `settings` file
# before creating any migrations or running manage.py migrate for the first time.

# If you have executed the first `$ python manage.py migrate` command
# after initializing the Django project and before creating a custom user model:
# reference：https://stackoverflow.com/questions/44651760/
# 1. Delete the _pycache_ and the 0001_initial files.
# 2. Delete the db.sqlite3 from the root directory.
# 3. Rerun: $ python manage.py makemigrations and $ python manage.py migrate


from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    pass
