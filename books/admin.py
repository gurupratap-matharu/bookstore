from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Book, Review


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "price", "download")

    def download(self, obj):
        url = obj.link
        html = f'<a href="{url}" target="_blank">Link</a>' if url else ""
        return mark_safe(html)  # nosec


@admin.register(Review)
class ReviewInline(admin.ModelAdmin):
    list_display = ("book", "review")
