# docs.djangoproject.com/en/3.2/topics/auth/customizing/#substituting-a-custom-user-model
# If you’re starting a new project, it’s highly recommended to set up
# a custom user model,even if the default User model is sufficient for you.


from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    pass
