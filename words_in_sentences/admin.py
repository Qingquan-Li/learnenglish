from django.contrib import admin

from .models import Tag, Sentence, Review

admin.site.register(Tag)


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 0
    readonly_fields = (
        'modified_time',
        'last_review_date',
    )


class SentenceAdmin(admin.ModelAdmin):
    # docs.djangoproject.com/en/3.2/ref/contrib/admin/#inlinemodeladmin-objects
    inlines = [ReviewInline]

    prepopulated_fields = {'slug': ('highlight_word', )}

    # docs.djangoproject.com/en/3.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.save_model
    # books.agiliq.com/projects/django-admin-cookbook/en/latest/current_user.html
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

    fieldsets = (
        (None, {
            'fields': (
                'is_active',
                'english_sentence',
                'highlight_word',
                'slug',
                'chinese_translation',
                'original_source',
                'note',
                'tags',
                'publish_date',
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
        'english_sentence',
        'highlight_word',
    )

    list_filter = (
        'tags',
        'publish_date',
    )

    search_fields = (
        'english_sentence',
        'highlight_word',
        'chinese_translation',
    )


admin.site.register(Sentence, SentenceAdmin)
