from datetime import date

from django.db import models
from django.urls import reverse

# from django.contrib.auth.models import User
from accounts.models import CustomUser


class CommonInfo(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    version = models.PositiveSmallIntegerField(default=0, editable=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    # docs.djangoproject.com/en/3.2/topics/db/models/#overriding-model-methods
    def save(self, *args, **kwargs):
        self.version = self.version + 1
        super().save(*args, **kwargs)  # Call the "real" save() method.


class Tag(models.Model):
    # docs.djangoproject.com/en/3.2/topics/db/models/#automatic-primary-key-fields
    # id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-id']

    # docs.djangoproject.com/en/3.2/ref/models/instances/#get-absolute-url
    def get_absolute_url(self):
        return reverse('api_v1_words_in_sentences:tag-detail',
                       kwargs={'pk': self.pk})
        # return reverse('words_in_sentences:tag-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


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
    author = models.ForeignKey(to=CustomUser,
                               on_delete=models.SET_NULL,
                               to_field='id',
                               blank=True,
                               null=True,
                               editable=False)
    # publish_at = models.DateTimeField(default=timezone.now)
    # Assuming you are in New York, and you use the defalt `TIME_ZONE = 'UTC'`, the admin page
    # will remind you as shown below until you configure `TIME_ZONE = 'America/New_York'`:
    # Note: You are 4 hours behind server time.
    publish_date = models.DateField(default=date.today)

    class Meta:
        ordering = ['-id']

    # docs.djangoproject.com/en/3.2/ref/models/instances/#get-absolute-url
    def get_absolute_url(self):
        # return reverse('api_v1_words_in_sentences:sentence-detail', kwargs={'pk': self.pk})
        return reverse('words_in_sentences:sentence-detail-with-slug',
                       kwargs={
                           'pk': self.pk,
                           'slug': self.slug
                       })

    def __str__(self):
        return self.english_sentence


class Review(models.Model):
    # docs.djangoproject.com/en/3.2/topics/db/models/#automatic-primary-key-fields
    # id = models.BigAutoField(primary_key=True)
    sentence = models.ForeignKey(to=Sentence,
                                 on_delete=models.CASCADE,
                                 to_field='id')
    review_times = models.PositiveSmallIntegerField(default=0)
    modified_time = models.DateTimeField(auto_now=True)
    last_review_date = models.DateField(auto_now=True)

    # docs.djangoproject.com/en/3.2/topics/db/models/#overriding-model-methods
    def save(self, *args, **kwargs):
        self.version = self.version + 1
        super().save(*args, **kwargs)  # Call the "real" save() method.
