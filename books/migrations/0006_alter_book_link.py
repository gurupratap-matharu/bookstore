# Generated by Django 4.2 on 2023-04-24 00:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0005_alter_book_author_alter_book_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="link",
            field=models.URLField(
                blank=True, max_length=500, null=True, verbose_name="Download Link"
            ),
        ),
    ]