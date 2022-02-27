from django.contrib import admin

from .models import Tag, Sentence

admin.site.register(Tag)


class SentenceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('highlight_word',)}

    # docs.djangoproject.com/en/3.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.save_model
    # books.agiliq.com/projects/django-admin-cookbook/en/latest/current_user.html
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)

    list_display = ('english_sentence', 'highlight_word',)

    list_filter = ('tags', 'publish_date',)

    search_fields = ('english_sentence', 'highlight_word', 'chinese_translation',)


admin.site.register(Sentence, SentenceAdmin)
