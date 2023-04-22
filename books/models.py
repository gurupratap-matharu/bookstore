import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=500)
    description = models.TextField()
    author = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    cover = models.ImageField(upload_to="covers/", blank=True)
    link = models.URLField(verbose_name=_("Download Link"), blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("special_status", "Can read all books"),
        ]
        ordering = ("-created_on",)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("books:book_detail", args=[str(self.id)])


class Review(models.Model):
    author = models.ForeignKey(
        get_user_model(), related_name="author", on_delete=models.CASCADE
    )
    book = models.ForeignKey(Book, related_name="reviews", on_delete=models.CASCADE)
    review = models.CharField(max_length=255)

    def __str__(self):
        return self.review
