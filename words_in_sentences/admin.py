from django.contrib import admin

from .models import Tag, Sentence

admin.site.register(Tag)


class SentenceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('highlight_word',)}


admin.site.register(Sentence, SentenceAdmin)
