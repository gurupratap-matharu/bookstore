# Generated by Django 4.2 on 2023-04-14 18:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="created_on",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="book",
            name="description",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="book",
            name="link",
            field=models.URLField(blank=True, null=True, verbose_name="Download Link"),
        ),
        migrations.AddField(
            model_name="book",
            name="updated_on",
            field=models.DateTimeField(auto_now=True),
        ),
    ]