# docs.djangoproject.com/en/3.2/topics/auth/customizing/#substituting-a-custom-user-model

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    pass
