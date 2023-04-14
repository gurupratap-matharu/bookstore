from django.contrib import admin

from .models import Book, Review


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "price")


@admin.register(Review)
class ReviewInline(admin.ModelAdmin):
    list_display = ("book", "review")
