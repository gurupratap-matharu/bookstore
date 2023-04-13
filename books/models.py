import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    cover = models.ImageField(upload_to="covers/", blank=True)

    class Meta:
        permissions = [
            ("special_status", "Can read all books"),
        ]

    def __str__(self):
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
