from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField

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
    # def get_absolute_url(self):
    # return reverse('speech:tag-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Article(CommonInfo):
    # docs.djangoproject.com/en/3.2/topics/db/models/#automatic-primary-key-fields
    # id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    # body = models.TextField(blank=True, null=True)
    body = RichTextField(blank=True, null=True)
    tags = models.ManyToManyField(to=Tag, blank=True)  # blank is stored as ''
    # ERRORS:
    # speech.Article.author: (fields.E304) Reverse accessor for 'speech.Article.author' clashes with
    # reverse accessor for 'writing.Article.author'.
    # HINT: Add or change a related_name argument to the definition for 'speech.Article.author'
    # or 'writing.Article.author'.
    author = models.ForeignKey(to=CustomUser,
                               on_delete=models.SET_NULL,
                               related_name='speech_article',
                               to_field='id',
                               null=True,
                               editable=False)

    class Meta:
        ordering = ['-id']

    # docs.djangoproject.com/en/3.2/ref/models/instances/#get-absolute-url
    def get_absolute_url(self):
        return reverse('speech:speech-article-detail-with-slug',
                       kwargs={
                           'pk': self.pk,
                           'slug': self.slug
                       })

    def __str__(self):
        return self.title
