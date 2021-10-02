from django.contrib import admin

from .models import Tag, Sentence

admin.site.register(Tag)


class SentenceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('highlight_word',)}

    # TODO request.user -> CustomUser
    # docs.djangoproject.com/en/3.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.save_model
    # books.agiliq.com/projects/django-admin-cookbook/en/latest/current_user.html
    # def save_model(self, request, obj, form, change):
    #     obj.created_by = request.user
    #     super().save_model(request, obj, form, change)


admin.site.register(Sentence, SentenceAdmin)
