# Generated by Django 3.2.9 on 2022-02-25 04:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('words_in_sentences', '0002_alter_tag_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sentence',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['-id']},
        ),
        migrations.AlterField(
            model_name='sentence',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]