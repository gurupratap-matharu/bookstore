import factory
from factory import fuzzy

from .models import Book


class BookFactory(factory.django.DjangoModelFactory):
    """
    Factory class that produces random books.
    """

    class Meta:
        model = Book
        django_get_or_create = ("title",)

    title = factory.Faker("catch_phrase")
    description = factory.Faker("paragraph", nb_sentences=10)
    author = factory.Faker("name")
    price = fuzzy.FuzzyDecimal(low=1, high=2000)
    link = factory.Faker("url")
