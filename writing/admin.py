from django.contrib import admin

from .models import Tag, Article

admin.site.register(Tag)


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}

    # docs.djangoproject.com/en/3.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.save_model
    # books.agiliq.com/projects/django-admin-cookbook/en/latest/current_user.html
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'slug',
                'summary',
                'body',
                'tags',
            )
        }),
        ('Readonly fields', {
            'classes': ('wide', 'extrapretty'),
            'fields': (
                'created_time',
                'modified_time',
                'version',
            ),
        }),
    )

    readonly_fields = (
        'created_time',
        'modified_time',
        'version',
    )

    list_display = (
        'title',
    )

    list_filter = (
        'tags',
        'created_time',
    )

    search_fields = (
        'title',
        'body',
    )


admin.site.register(Article, ArticleAdmin)
