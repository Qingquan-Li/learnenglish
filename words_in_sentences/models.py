from datetime import date

from django.db import models
# from django.contrib.auth.models import User
from accounts.models import CustomUser


class CommonInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    version = models.PositiveSmallIntegerField(default=0, editable=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # docs.djangoproject.com/en/3.2/topics/db/models/#overriding-model-methods
        self.version = self.version + 1
        # super(SubscribeMsg, self).save(*args, **kwargs)
        super().save(*args, **kwargs)  # Call the "real" save() method.


class Tag(models.Model):
    # docs.djangoproject.com/en/3.2/topics/db/models/#automatic-primary-key-fields
    # id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)


class Sentence(CommonInfo):
    # docs.djangoproject.com/en/3.2/topics/db/models/#automatic-primary-key-fields
    # id = models.BigAutoField(primary_key=True)
    english_sentence = models.TextField()
    highlight_word = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    chinese_translation = models.TextField(blank=True, null=True)
    original_source = models.URLField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(to=Tag, blank=True)
    created_by = models.ForeignKey(to=CustomUser, on_delete=models.SET_NULL,
                                   to_field='id', blank=True, null=True)
    # publish_at = models.DateTimeField(default=timezone.now)
    # If you are in New York, the admin interface will remind you:
    # Note: You are 4 hours behind server time.
    publish_date = models.DateField(default=date.today)
    is_understand = models.BooleanField(default=False)

    def __str__(self):
        return self.english_sentence
